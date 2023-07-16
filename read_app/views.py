from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

# Views
def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        return render(request, 'home.html', {'user_first_name': current_user.first_name})
    else:
        return render(request, 'home.html')

def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, 'User not registered')
            return redirect('login')
    # Render the page
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered! Welcome!')
            return redirect('home')

    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def toForgotPage(request):
    return render(request, 'forgot.html')

def toOtpPage(request):
    return render(request, 'confirm_otp.html')


    
