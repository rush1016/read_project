from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def toLoginPage(request):
    return render(request, 'login.html')

def toRegisterPage(request):
    return render(request, 'register.html')

def toForgotPage(request):
    return render(request, 'forgot.html')