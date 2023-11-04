from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.db import transaction

from read_app.models import User
from students.models import Student
from assessment.models import ( 
    AssessmentSession, 
    AssessmentSessionPassage, 
    ScreeningAssessment, 
    GradedAssessment 
)
from materials.models import Passage, AssessmentPreset


@transaction.atomic
def assign_assessment(request, assessment_type):
    if request.method == 'POST':
        student_list = request.POST.getlist('selected_records')

        for student in student_list:
            student_user_instance = get_object_or_404(User, pk=student)
            student_instance = get_object_or_404(Student, user=student_user_instance)
            assessment_session = AssessmentSession.objects.create(
                student = student_instance,
                assessment_type = assessment_type,
                grade_level = student_instance.grade_level,
            )

            assign_assessment_type(assessment_session, request)

            assessment_session.save()
            messages.success(request, 'Successfully assigned assessment.')
         
    return redirect('assessment_select')


def assign_assessment_type(assessment_session, request):
    if assessment_session.assessment_type == 'Screening':
        preset_id = request.POST.get('preset_select')
        assign_screening(assessment_session, preset_id)
        assessment_session.student.screening = True
        assessment_session.student.save()
    elif assessment_session.assessment_type == 'Graded':
        passage_id = request.POST.get('passage_id')
        assign_graded(assessment_session, passage_id)


def assign_screening(assessment_session, preset_id):
    preset = get_object_or_404(AssessmentPreset, pk=preset_id)
    passages = get_list_or_404(Passage, preset=preset)
    total_questions = 0
    order = 1
    for passage in passages:
        create_assessment_session_passage(assessment_session, passage, order)
        order += 1
        total_questions += len(passage.get_questions())

    assessment_session.number_of_questions = total_questions
    assessment_session.save()

    screening_assessment_instance = ScreeningAssessment.objects.create(
        assessment_session = assessment_session
    )
    screening_assessment_instance.update_question_counts() 


def assign_graded(assessment_session, passage_id):
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    assessment_session.number_of_questions = len(passage_instance.get_questions())
    assessment_session.save()

    create_assessment_session_passage(assessment_session, passage_instance, 1)

    GradedAssessment.objects.create(
        assessment_session = assessment_session
    )    


def create_assessment_session_passage(assessment_session, passage, order):
    AssessmentSessionPassage.objects.create(
        assessment_session = assessment_session,
        order = order,
        passage = passage,
    )