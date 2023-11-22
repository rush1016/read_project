from django.contrib.auth.forms import PasswordChangeForm
from django import forms

class PasswordChangeCustomForm(PasswordChangeForm):
        old_password = forms.CharField(
            required=True, 
            label='Old password',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your old/current password'
                    }
            ),
            error_messages={
                'required': 'The password cannot be empty'
            }
        )

        new_password1 = forms.CharField(
            required=True, 
            label='New Password',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your desired new password',
                }
            ),
            error_messages={
                'required': 'The password cannot be empty'
            }
        )
        new_password2 = forms.CharField(
            required=True, 
            label='Confirm password',
            widget=forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Please re-type your new password',
                }
            ),
            error_messages={
                'required': 'The password cannot be empty'
            }
        )