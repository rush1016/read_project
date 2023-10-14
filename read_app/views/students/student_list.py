from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from read_app.models import User, Student
from read_app.forms.students import StudentRegistrationForm
from read_app.forms.approve import ApprovalForm

# Student Records Views
@login_required
def student_list(request):
    # Create an instance to use as ForeignKey
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(teacher=teacher_instance).order_by('student_id')
    print(students)
    approval_form = ApprovalForm()
    context = {
        'students': students,
        'teacher_code': teacher_instance.teacher.teacher_code,
        'approval_form': approval_form,
    }
    return render(request, 'students/student_list.html', context)

