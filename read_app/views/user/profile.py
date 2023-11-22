from django.shortcuts import render

from read_app.forms.email import ChangeEmailForm
from read_app.forms.password_change import PasswordChangeCustomForm

def teacher_profile_view(request):
    email_form = ChangeEmailForm(user=request.user)
    password_form = PasswordChangeCustomForm(user=request.user)

    context = {
        'email_form': email_form,
        'password_form': password_form
    }

    return render(request, 'teachers/teacher_profile.html', context)