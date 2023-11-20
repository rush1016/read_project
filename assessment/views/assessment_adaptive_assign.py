from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages

from students.models import Student
from materials.models import Passage
from assessment.models import AssessmentSession

from assessment.views.assessment_assign import assign_assessment_type
from utils.generate_passcode import generate_passcode

def assign_recommended_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    passcode = generate_passcode()


    if request.method == "POST":
        type = request.POST.get('type')

        if type == 'Screening':
            if not student.student_rating.english_gst_score or not student.student_rating.filipino_gst_score:
                assign_screening(student, request)
                return redirect('student_profile', student.id)

        elif type == 'Graded':
            passage_id = request.POST.get('passage_id')
            passage = Passage.objects.get(pk=passage_id)
            assessment_type = 'Graded'

            assessment_session = AssessmentSession.objects.create(
                student = student,
                assessment_type = assessment_type,
                grade_level = passage.grade_level,
                passcode = passcode
            )
            assign_assessment_type(assessment_session, request)

            messages.success(request, f'Successfully assigned material. Use this code to conduct the assessment {passcode}') 
            return redirect('assessment_session', assessment_session.id)


    elif request.method == "GET":
        language = request.GET.get('language-selected')
        print('language:', language)
        # Set the recommended grade level based on the students recommended grade_level
        if language == 'English':
            student_recommended_grade = student.student_rating.english_recommended_grade
        elif language == 'Filipino':
            student_recommended_grade = student.student_rating.filipino_recommended_grade

        passages = Passage.objects.filter(grade_level=student_recommended_grade, preset=None, language=language).exclude(
            # Exclude materials that have already been assigned
            assessment_passage__assessment_session__student=student,
            assessment_passage__assessment_session__is_finished=False
        ).order_by('set')

        
    language = request.GET.get('language-selected')

    context = {
        'student': student,
        'passages': passages,
        'language': language,
    }

    return render(request, 'assessment/recommended_materials.html', context)


def assign_screening(student, request):
    passcode = generate_passcode()
    assessment_type = 'Screening'
    assessment_session = AssessmentSession.objects.create(
        student = student,
        assessment_type = assessment_type,
        grade_level = student.grade_level,
        passcode = passcode
    )
    assign_assessment_type(assessment_session, request)
    assessment_session.save()
        
    messages.success(request, f'Successfully assigned assessment.\nCopy this code to and enter it in the assessment code field: {assessment_session.passcode}')