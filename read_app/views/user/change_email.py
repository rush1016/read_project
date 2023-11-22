from django.shortcuts import redirect
from django.contrib import messages

from read_app.forms.email import ChangeEmailForm

def change_email_view(request):
    if request.method == 'POST':
        form = ChangeEmailForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Successfully changed email.')

        else:
            error_messages = ' '.join(' '.join(errors) for field, errors in form.errors.items())
            messages.error(request, error_messages)

    return redirect('teacher_profile')
            
