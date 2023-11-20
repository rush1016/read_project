from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from read_app.models import User
from students.models import Student
from students.forms.students import StudentRegistrationForm

# Student Records Views
@login_required
def student_list(request):
    # Create an instance to use as ForeignKey
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = get_student_list(teacher_instance)
    add_form = StudentRegistrationForm 
    context = {
        'students': students,
        'add_form': add_form,
    }
    return render(request, 'students/student_list.html', context)


def get_student_list(teacher_instance):
    students = Student.objects.filter(teacher=teacher_instance).order_by('-date_added', '-id')

    return students
