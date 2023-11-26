from django.shortcuts import redirect
from django.contrib import messages

from read_app.forms.username_change import ChangeUsernameForm

def change_username_view(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()

            messages.success(request, 'Successfully changed Username.')

        else:
            error_messages = ' '.join(' '.join(errors) for field, errors in form.errors.items())
            messages.error(request, error_messages)

    return redirect('teacher_profile')
            
