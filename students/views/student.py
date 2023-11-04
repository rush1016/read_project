from django.shortcuts import render, get_object_or_404, get_list_or_404

from read_app.models import User
from assessment.models import AssessmentSession

def student_profile_view(request, student_id):
    student_user = get_object_or_404(User, pk=student_id)
    student_instance = student_user.student_instance
    assessments = student_instance.get_assessments()

    context = {
        'student': student_instance,
        'assessments': assessments,
    }

    return render(request, 'students/student_profile.html', context)