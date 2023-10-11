from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from read_app.models import User, Student

# Student Records Views
@login_required
def student_list(request):
    # Create an instance to use as ForeignKey
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(teacher=teacher_instance).order_by('student_id')
    context = {
        'students': students,
    }
    return render(request, 'students/student_list.html', context)

