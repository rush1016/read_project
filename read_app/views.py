from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.db import transaction
from .forms.students import StudentRegistrationForm
from .forms.teachers import TeacherRegistrationForm
from .models import Student, ClassSection, ArchivedStudent
import datetime


# Account Handling Views 
def home(request):
    return render(request, 'home.html')


def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        email_or_username = request.POST['email']
        password = request.POST['password']

        # Check if user exists
        user = authenticate(request, username=email_or_username, password=password)
        if user is not None:
            login(request, user) # Log in using Django's built-in app
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login credentials')
            return redirect('login')
   
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'registration/login.html')


def logout_user(request):
    logout(request) # Django's built-in logout function from authentication app
    messages.success(request, "You have been logged out!")
    
    return redirect('home')


""" def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome!')
            return redirect('home') 
        else:
            messages.error(request, 'An error occurred. Please check the requirements.') 
    
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm()
    return render(request, 'registration/register.html', {'registerForm': form}) """


def registration(request):
    return render(request, 'registration/signup_role_select.html')


def student_registration(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
        else:
            messages.error(request, form.errors)


    form = StudentRegistrationForm()
    context = {
        'register_form': form
    }
    return render(request, 'registration/signup_student.html', context)


def teacher_registration(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)

        if form.is_valid():
            form.save() # Save the account into the database

            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user) # Login the user before redirecting to homepage

            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
        
        else:
            messages.error(request, form.errors)
    
    form = TeacherRegistrationForm()
    context = {
        'register_form': form
    }
    return render(request, 'registration/signup_teacher.html', context)


def forgot_password_request(request):
    return render(request, 'registration/forgot.html')


#########################################################
# Student Records Views
@login_required
def student_list(request):
    students = Student.objects.filter(teacher_id=request.user.id).order_by('id')
    context = {
        'students': students,
    }
    return render(request, 'student_list.html', context)


def check_archived_student(student_data):
    # Check if an archived student with the same details exists.
    archived_student = ArchivedStudent.objects.filter(
        first_name=student_data['first_name'],
        last_name=student_data['last_name'],
        grade_level=student_data['grade_level'],
        class_section=student_data['class_section']
    ).first()
    return archived_student


""" def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

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

    return redirect('student_list') """


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


""" def edit_student(request, student_id):
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
            return redirect('../student_list') """


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
    return redirect('student_list')



# For fetching data from the database
def get_student_info(request, student_id):
    try:
        # Retrieve the student record
        student = get_object_or_404(Student, pk=student_id)
        student_data = {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'grade_level': student.grade_level,
            'class_section': student.class_section, 
        }

        return JsonResponse({'success': True, 'student_data': student_data})

    except Http404:
        # Handle the case where the student record is not found
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)


def get_class_section_data(request):
    try:
        class_section_data = ClassSection.objects.values('grade_level', 'section_name')
        return JsonResponse({'class_section_data': list(class_section_data)})

    except Exception as e:
        # Handle any exceptions that might occur during database query or JSON serialization
        return JsonResponse({'success': False, 'error': str(e)}, status=500)