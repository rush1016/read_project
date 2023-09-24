from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import RegisterForm, StudentForm
from .models import Student

# Account Handling Views 
def home(request):
    return render(request, 'home.html')

def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        email_or_username = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email_or_username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, 'Invalid Login credentials')
            return redirect('login')
   
    # Render the page
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
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
    
    return render(request, 'register.html', {'form': form})


def forgot_password(request):
    return render(request, 'forgot.html')


# Student Records Views
@login_required
def student_list(request):
    students = Student.objects.filter(teacher_id=request.user.id)
    form = StudentForm()

    context = {
        'students': students,
        'form': form,
    }
    
    return render(request, 'student_list.html', context)

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)
            student.teacher_id = request.user.id
            student.save()

            # Get the updated student list as HTML
            students = Student.objects.filter(teacher_id=request.user.id)
            html_student_list = render_to_string('partial_student_table.html', {'students': students})

            return JsonResponse({'success': True, 'html_student_list': html_student_list})
    
    return JsonResponse({'success': False, 'errors': form.errors})