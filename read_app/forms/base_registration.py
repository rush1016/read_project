from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from read_app.models import User
from string import capwords

# For unique username generator
from django.utils.text import slugify


class BaseRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Email Address (Optional)'}))
    first_name = forms.CharField(
        label="", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'First Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid first name containing only letters, spaces, hyphens, and apostrophes.',)])
    last_name = forms.CharField(
        label="", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Last Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid last name containing only letters, spaces, hyphens, and apostrophes.',)])
    """
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Username'
            }
        )
    )
    """
    
    password1 = forms.CharField( # First password input
        label="",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>')
    password2 = forms.CharField( # Confirm password input
        label="",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text= '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    # Override clean methods to convert to Title Case / Capital first letter
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capwords(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capwords(last_name)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email 
    
    def generate_unique_username(self, first_name, last_name):
        first_name = first_name.lower()
        last_name = last_name.lower()

        # Generate a unique username based on first name, last name, grade level, and section
        base_username = slugify(f"{first_name}{last_name}")
        
        if not User.objects.filter(username=base_username).exists():
                return base_username

        # If the base username exists, find the next available incrementing number
        i = 1
        while True:
            username = f"{base_username}{i}"
            if not User.objects.filter(username=username).exists():
                return username
            i += 1