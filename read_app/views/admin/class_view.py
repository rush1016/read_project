from django.shortcuts import render

from read_app.models import User, Teacher
from students.models import Student

def class_view(request, teacher_user_id):
    teacher_user = User.objects.get(pk=teacher_user_id)
    students = Student.objects.filter(teacher=teacher_user)

    context = {
        'students': students,
        'teacher_user': teacher_user,
    }

    return render(request, 'admin/class_view.html', context)