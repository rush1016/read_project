from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

from read_app.models import User

class ChangeUsernameForm(forms.Form):
    password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please type your current password.'
            }
        )
    )

    new_username = forms.CharField(
        label='New Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please type your new desired username.'
            }
        ),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeUsernameForm, self).__init__(*args, **kwargs)

    def clean_new_username(self):
        new_username = self.cleaned_data["new_username"]
        if not new_username:
            return new_username

        # Check for the existence of a user with the new username
        if User.objects.filter(username=new_username).exists():
            raise ValidationError("A user with this username already exists!")

        # Check additional requirements for the username
        validator = UnicodeUsernameValidator()
        try:
            validator(new_username)
        except ValidationError as e:
            raise ValidationError(e.message)

        return new_username

    def clean_password(self):
        user = self.user
        password = self.cleaned_data['password']

        if not user.check_password(password):
            raise ValidationError("Incorrect password.")

    def save(self):
        # Update the username field of the user model
        user = self.user
        user.username = self.clean_new_username()
        user.save()
