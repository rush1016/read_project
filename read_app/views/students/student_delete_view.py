from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.decorators import login_required

from read_app.forms.student_edit import StudentEditForm
from read_app.models import User, Teacher, Student, ArchivedStudent

@login_required
@transaction.atomic
def student_delete(request, student_id):
    student_user_instance = get_object_or_404(User, pk=student_id)
    student_instance = get_object_or_404(Student, user=student_user_instance)

    if request.method == 'POST':
        # Archive the deleted student record 
        archive_student_instance = ArchivedStudent.objects.create(
            previous_teacher = student_instance.teacher,
            first_name = student_instance.first_name,
            last_name = student_instance.last_name,
            student_id = student_instance.student_id,
            student_lrn = student_instance.student_lrn,
            grade_level = student_instance.grade_level,
            class_section = student_instance.class_section,
            date_added = student_instance.date_added,
            is_approved = student_instance.is_approved,
        )
        archive_student_instance.save()
        student_instance.delete()
        return redirect('student_list')

    else:
        student_form = StudentEditForm(instance=student_instance)
        student_id = student_user_instance.id

        context = {
            'student_form': student_form,
            'student_id': student_id,
        }
        return render(request, 'students/partials/partial_student_delete_form.html', context)


