from django.shortcuts import render, redirect
from django.contrib import messages
from students.forms.students import StudentRegistrationForm
from read_app.forms.teachers import TeacherRegistrationForm
from django.contrib.auth import authenticate, login


def register(request):

    return render(request, 'registration/signup_role_select.html')


def login_after_register(request, form):
    email = form.cleaned_data['email']
    password = form.cleaned_data['password1']
    user = authenticate(username=email, password=password)
    login(request, user) # Login the user before redirecting to homepage


def student_register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            
            login_after_register(request, form)

            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
        else:
            errors = form.errors

            for field_name, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, error)

            context = {
                'register_form': form
            }
            return render(request, 'registration/signup_student.html', context)

    form = StudentRegistrationForm()
    context = {
        'register_form': form
    }
    return render(request, 'registration/signup_student.html', context)


def teacher_register(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)

        if form.is_valid():
            form.save() # Save the account into the database

            login_after_register(request, form)

            messages.success(request, "You have successfully registered! Welcome!")
            return redirect('home')
        
        else:
            context = {
                'register_form': form
            }
            return render(request, 'registration/signup_teacher.html', context )
    
    form = TeacherRegistrationForm()
    context = {
        'register_form': form
    }
    return render(request, 'registration/signup_teacher.html', context)