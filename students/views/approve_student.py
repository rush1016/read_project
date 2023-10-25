from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from read_app.models import User
from students.models import Student
from students.forms.approve import ApprovalForm


def approve_student(request, student_id):
    print('hello!')
    student_user_instance = get_object_or_404(User, pk=student_id)
    student_instance = get_object_or_404(Student, user=student_user_instance)
    print('instance: ', student_user_instance)
    print('student: ', student_instance)
    if request.method == 'POST':
        approve_form = ApprovalForm(request.POST, instance=student_instance)
        if approve_form.is_valid():
            approve_form.save()
            messages.success(request, "Student Registration Approved!")
        else:
            messages.error(request, approve_form.errors)
            print(approve_form.errors)


        return redirect('student_list')
    
    else:
        approve_form = ApprovalForm(instance=student_instance)

        context = {
            'approve_form': approve_form,
            'student_id': student_id,
        }

        return render(request, 'students/partials/partial_student_approve_form.html', context)
