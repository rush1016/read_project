from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from .forms import RegisterForm, StudentForm
from .models import Student, ClassSection


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
   
    else:
        return render(request, 'registration/login.html')


def logout_user(request):
    logout(request) # Django's built-in logout function from authentication app
    messages.success(request, "You have been logged out!")
    
    return redirect('home')


def register_user(request):
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
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'registerForm': form})


def forgot_password(request):
    return render(request, 'registration/forgot.html')



# Student Records Views
@login_required
def student_list(request):
    students = Student.objects.filter(teacher_id=request.user.id).order_by('id')
    addStudentForm = StudentForm()
    editStudentForm = StudentForm()
    context = {
        'students': students,
        # Forms
        'addStudentForm': addStudentForm,
        'editStudentForm': editStudentForm,
    }
    
    return render(request, 'student_list.html', context)


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.teacher_id = request.user.id
            student.save()
            messages.success(request, 'Student record successfully added')

            return redirect('student_list')
        else:
            messages.error(request, form.errors)

            return redirect('student_list')

    else:
        form = StudentForm()
   
        messages.error(request, form.errors) 
        return redirect('student_list')


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

        return JsonResponse({'success': True, 'data': student_data})

    except Http404:
        # Handle the case where the student record is not found
        return JsonResponse({'success': False, 'error': 'Student not found'}, status=404)


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
    # Get the student object to delete
    student = get_object_or_404(Student, id=student_id)

    # Check if the student belongs to the logged-in teacher
    if student.teacher_id == request.user.id:
        student.delete()
        messages.success(request, 'Student record deleted.')
        return redirect('student_list')

    messages.error(request, "An error occured.")
    return redirect('student_list')


def get_class_section_data(request):
    class_section_data = ClassSection.objects.values('grade_level', 'section_name')
    return JsonResponse({'class_section_data': list(class_section_data)})