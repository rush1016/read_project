from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required

from read_app.models import User, Teacher
from students.models import Student, ArchivedStudent
from students.forms.student_edit import StudentEditForm

@login_required
@transaction.atomic
def student_delete(request, student_id):
    student_instance = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        student_instance.delete()
        return redirect('student_list')