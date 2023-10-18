from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from read_app.models import User, Student, AssessmentSession

def select(request):
    return render(request, 'assessment/assessment_select.html')

@transaction.atomic
def select_student_screening(request):
    teacher_instance = User.objects.get(pk=request.user.id, is_teacher=True)
    students = Student.objects.filter(teacher=teacher_instance, assessments_done=0, has_ongoing_assessment=False).order_by('student_id')

    context = {
        'students': students,
    }
    return render(request, 'assessment/assessment_student_select.html', context)

@transaction.atomic
def assign_screening_assessment(request):
    student_list = request.POST.getlist('selected_records')

    for student in student_list:
        print('student: ', student)
        student_user_instance = get_object_or_404(User, pk=student)
        student_instance = get_object_or_404(Student, user=student_user_instance)
        assign_student = AssessmentSession.objects.create(
            student = student_user_instance,
            assessment_type = 'Screening',
            grade_level = student_instance.grade_level,
        )
        student_instance.has_ongoing_assessment = True

        student_instance.save()
        assign_student.save()
        messages.success(request, 'Successfully assigned assessment.')
         
    return redirect('assessment/screening/select_student')