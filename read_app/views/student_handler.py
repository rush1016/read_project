""" 
from read_app.forms.students import StudentRegistrationForm


def add_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.teacher_id = request.user.id

            student_data = {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'grade_level': student.grade_level,
                'class_section': student.class_section,
            }

            archived_student = check_archived_student(student_data)

            # A matching archived student record exists
            if archived_student:
                return JsonResponse({'archived_student_id': archived_student.id})
            
            student.save()
            messages.success(request, 'Student record successfully added')
            return JsonResponse({'success': True})
        
        messages.error(request, form.errors)
        return JsonResponse({'success': False, 'errors': form.errors})

    return redirect('student_list')


def check_archived_student(student_data):
    # Check if an archived student with the same details exists.
    archived_student = ArchivedStudent.objects.filter(
        first_name=student_data['first_name'],
        last_name=student_data['last_name'],
        grade_level=student_data['grade_level'],
        class_section=student_data['class_section']
    ).first()
    return archived_student


def confirm_add_archived_student(request, archived_student_id):
    archived_student = get_object_or_404(ArchivedStudent, pk=archived_student_id)

    # Check if the archived student was added by the current user
    if archived_student.teacher_id != request.user.id:
        messages.error(request, 'Permission denied to add this archived student.')
        return redirect('student_list')

    # Create an archived student record
    student = Student(
        id=archived_student.id,
        teacher=request.user,
        first_name=archived_student.first_name,
        last_name=archived_student.last_name,
        grade_level=archived_student.grade_level,
        class_section=archived_student.class_section,
        date_added=datetime.date.today(),
    )

    # To group database operations into a single transaction
    # and maintain consistency and integrity of the database
    with transaction.atomic(): 
        student.save()
        archived_student.delete()

    messages.success(request, 'Archived student added to active records.')
    return redirect('student_list')


def edit_student(request, student_id):
    if request.method == 'POST':
        # Retrieve the student record
        student = get_object_or_404(Student, pk=student_id)
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            # Form is accepted
            form.save()
            messages.success(request, 'Student record edited.')

            return redirect('../student_list')
        else:
            # Form validation failed
            if (form.errors.get('first_name')):
                formError = form.errors.get('first_name')
            elif (form.errors.get('last_name')):
                formError = form.errors.get('last_name')
            formError = form.errors

            messages.error(request, formError)
            return redirect('../student_list')


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Create an archived student record
    archived_student = ArchivedStudent(
        id=student.id,
        teacher_id=request.user.id,
        first_name=student.first_name,
        last_name=student.last_name,
        grade_level=student.grade_level,
        class_section=student.class_section,
    )

    # To group database operations into a single transaction
    # and maintain consistency and integrity of the database
    with transaction.atomic():
        archived_student.save()
        student.delete()

    messages.success(request, 'Student record archived and deleted.')
    return redirect('student_list') """