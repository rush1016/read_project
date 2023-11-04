from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect


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
    
    return redirect('login')