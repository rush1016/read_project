from django.shortcuts import render, get_object_or_404, get_list_or_404

from assessment.models import AssessmentSession
from read_app.models import User
from students.models import Student

def assessment_list_view(request):
    teacher_instance = get_object_or_404(User, pk=request.user.id, is_teacher=True)
    students = get_list_or_404(Student, teacher=teacher_instance)

    screening_assessments = AssessmentSession.objects.filter(student__in=students, assessment_type='Screening')
    graded_assessments = AssessmentSession.objects.filter(student__in=students, assessment_type='Graded')
    context = {
        'screening_assessments': screening_assessments,
        'graded_assessments': graded_assessments
    }

    return render(request, 'assessment/assessment_list.html', context)


def assessment_info_view(request, assessment_id):
    assessment_instance = get_object_or_404(AssessmentSession, pk=assessment_id)
    context = {
        'assessment_instance': assessment_instance,
    }

    return render(request, 'assssment/assessment_info.html', context)
    