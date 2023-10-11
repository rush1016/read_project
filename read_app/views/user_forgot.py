from django.shortcuts import render

def forgot_password_request(request):
    return render(request, 'registration/forgot.html')