from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.text import slugify

from string import capwords
# For unique username generator


from read_app.models import Teacher
from read_app.models import User, School, ClassSection

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        CLASS_SECTIONS = (
            (f'{section.grade_level}_{section.section_name}', f'Grade {section.grade_level} - {section.section_name}') for section in ClassSection.objects.all()
        )

        self.fields['class_section'].choices = CLASS_SECTIONS
        

    registration_code = forms.CharField(
        label="School Registration Code", 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'School Registration Code'}),
        help_text= '<span class="form-text text-muted"><small>Ask your school administrator for the Registration Code of your school.</small></span>'
    )
        

    email = forms.EmailField(
        label="Email", 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Email Address'}),
        required=True
    )
        
    first_name = forms.CharField(
        label="First Name", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'First Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid first name containing only letters, spaces, hyphens, and apostrophes.',)])
    last_name = forms.CharField(
        label="Last Name", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Last Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid last name containing only letters, spaces, hyphens, and apostrophes.',)])
    
    class_section = forms.ChoiceField(
        label="Grade and Section", 
        choices=[],
        widget=forms.Select(
            attrs={'class':'form-select'}),
        required=True,
    )
    password1 = forms.CharField( # First password input
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
    )
    password2 = forms.CharField( # Confirm password input
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Please type your password again'}),
        help_text= '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    )

    field_order = ['registration_code', 'first_name', 'last_name', 'class_section', 'email', 'password1', 'password2' ]
    # Override clean methods to convert to Title Case / Capital first letter
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capwords(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capwords(last_name)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            return email

        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        
        return email 
    
    def clean_registration_code(self):
        registration_code = self.cleaned_data['registration_code']
        try:
            school = School.objects.get(registration_code=registration_code)
            if school:
                return registration_code
            else:
                raise ValidationError('School code does not exists. Please confirm registration code with your school administrator')
        except:
            raise ValidationError('School code does not exists. Please confirm registration code with your school administrator')
    
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
    @transaction.atomic # Package the database operation to maintain data integrity.
    def save(self):
        # Save the Student account into the User model
        user = super().save(commit=False)
        username = self.generate_unique_username(
            user.first_name,
            user.last_name,
        )
        user.username = username
        user.is_teacher = True
        user.save()

        # And add the necessary data into their respective fields
        registration_code = self.clean_registration_code()
        school = School.objects.get(registration_code=registration_code)
        selected_section = self.cleaned_data['class_section']
        grade_level, section = selected_section.split('_')

        teacher = Teacher.objects.create(
            user = user, 
            school = school,
            grade_level = grade_level,
            section = section,
        )

        teacher.save()