from django.shortcuts import render, redirect
from django.contrib import messages
from read_app.forms.students import StudentRegistrationForm
from read_app.forms.teachers import TeacherRegistrationForm
from django.contrib.auth import authenticate, login


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