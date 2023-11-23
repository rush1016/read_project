from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from read_app.models import User
from students.models import Student
from students.forms.student_edit import StudentEditForm
from students.forms.students import StudentRegistrationForm

@login_required
def student_edit(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        student_form = StudentRegistrationForm(instance=student)
    except:
        messages.error(request, 'Record not found')
        return redirect('student_profile', student_id)

    if request.method == 'POST':
        student = Student.objects.get(pk=student_id)
        student_form = StudentRegistrationForm(request.POST, instance=student)
        if student_form.is_valid():
            teacher = request.user
            student_form.save(teacher=teacher)

            messages.success(request, 'Student record saved.')
        
        else:
            messages.error(request, 'Student record not saved.')
            messages.success(request, student_form.errors)
        
        return redirect('student_profile', student_id)