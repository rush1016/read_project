from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from read_app.models import User
from materials.models import Choice
from assessment.models import AssessmentSession, StudentAnswer

from assessment.forms.question import AssessmentQuestionForm

def student_assessment_list(request):
    student_user_instance = get_object_or_404(User, pk=request.user.id)
    student_instance = student_user_instance.student_instance
    assessment_sessions = AssessmentSession.objects.filter(student=student_instance, is_finished=False)
    context = {
        'assessment_sessions': assessment_sessions,
    }
    return render(request, 'assessment/student/assessment_list.html', context)