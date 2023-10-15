from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from read_app.forms.student_edit import StudentEditForm
from read_app.models import User, Student

def student_edit(request, student_id):
    student_user_instance = get_object_or_404(User, pk=student_id)
    student_instance = get_object_or_404(Student, user=student_user_instance)

    if request.method == 'POST':
        student_edit_form = StudentEditForm(request.POST, instance=student_instance)
        if student_edit_form.is_valid():
            student_edit_form.save()

            messages.success(request, 'Student record saved.')
            return redirect('student_list')
        
        else:
            messages.error(request, 'Student record not saved.')
            messages.success(request, student_edit_form.errors)
            return redirect('student_list')
        
    else:
        student_edit_form = StudentEditForm(instance=student_instance)

    context = {
        'student_edit_form': student_edit_form,
        'student_instance': student_instance,
    }

    return render(request, 'students/partial_student_edit_form.html', context)
        
