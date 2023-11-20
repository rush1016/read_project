from django.shortcuts import render, get_object_or_404, get_list_or_404

from assessment.models import AssessmentSession
from read_app.models import User
from students.models import Student

def assessment_list_view(request):
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(teacher=teacher_instance)

    screening_assessments = AssessmentSession.objects.filter(student__in=students, assessment_type='Screening').order_by('-assigned_time')
    graded_assessments = AssessmentSession.objects.filter(student__in=students, assessment_type='Graded').order_by('-assigned_time')
    context = {
        'screening_assessments': screening_assessments,
        'graded_assessments': graded_assessments
    }

    return render(request, 'assessment/assessment_list.html', context)


def assessment_info_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    assessment_passages = assessment_instance.get_passages()
    
    score = assessment_instance.total_score

    student_answers_dict = {}

    for passage in assessment_passages:
        passage_instance = passage.passage # Reverse relation
        student_answers = list(assessment_instance.student_answer.filter(passage=passage_instance))
        student_answers_dict[passage] = student_answers

    print(student_answers_dict)
    context = {
        'score': score,
        'student_answers': student_answers_dict,
        'assessment_instance': assessment_instance,
    }

    return render(request, 'assessment/assessment_info.html', context)
    