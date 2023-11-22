from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError

from read_app.forms.password_change import PasswordChangeCustomForm

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            # Update the user's session to prevent them from being logged out
            update_session_auth_hash(request, form.user)

            messages.success(request, 'Successfully changed password.')
        else:
            error_messages = ' '.join(' '.join(errors) for field, errors in form.errors.items())
            messages.error(request, error_messages)

    return redirect('teacher_profile')
            
