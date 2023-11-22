from django import forms
from django.core.exceptions import ValidationError

from read_app.models import User

class ChangeEmailForm(forms.Form):
    password = forms.CharField(
        label = 'Current Password',
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please type your current password.'
            }
        )
    )

    email = forms.EmailField(
        label = 'New Email',
        widget= forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please type your new desired email.'
            }
        ),
        required=True
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user

        super(ChangeEmailForm, self).__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            return email

        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        
        return email 

    def clean_password(self):
        user = self.user
        password = self.cleaned_data['password']

        if not user.check_password(password):
            raise ValidationError("Incorrect password.")
        

    def save(self):
        # Update the email field of the user model
        user = self.user

        user.email = self.clean_email()
        user.save()
