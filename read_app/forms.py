from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, password_validation
from django.core.validators import RegexValidator
from django.db import transaction
from django import forms
from .models import User, Teacher, Student, ClassSection
from string import capwords

# For unique username generator
from django.utils.text import slugify
import random
import string


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Email Address'}
        )
    )
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'First Name'}
        )
    )
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Last Name'}
        )
    )

    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Username'
            }
        )
    )

    password1 = forms.CharField( # First password input
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Password'
            }
        ),
        help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
    )

    password2 = forms.CharField( # Confirm password input
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Confirm Password'
            }
        ),
        help_text= '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Email Address'
            }
        )
    )
    first_name = forms.CharField(
        label="", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'First Name'
            }
        ),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid first name containing only letters, spaces, hyphens, and apostrophes.',
            )
        ]
    )
    last_name = forms.CharField(
        label="", 
        max_length=80, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Last Name'}
        ),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid last name containing only letters, spaces, hyphens, and apostrophes.',
            )
        ]
    )
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
            attrs={
                'class': 'form-control', 
                'placeholder': 'Password'
            }
        ),
        help_text='<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
    )
    password2 = forms.CharField( # Confirm password input
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Confirm Password'
            }
        ),
        help_text= '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
    )
    grade_level = forms.ChoiceField(
        choices=[], 
        label='Grade Level',
    )
    class_section = forms.ChoiceField(
        choices=[], 
        label='Section',
    )
    teacher = forms.ChoiceField(
        choices=[],
        label='Teacher',
        widget=forms.Select(
            attrs={
                'class': 'form-select',
                'required': 'required',
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'teacher', 'grade_level', 'class_section', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['grade_level'] = forms.ChoiceField(choices=[], label='Grade Level')
        self.fields['class_section'] = forms.ChoiceField(choices=[], label='Section')

        grade_level_choices = [
            (4, 'Grade 4'),
            (5, 'Grade 5'),
            (6, 'Grade 6'),
        ]
        # Get the class section data from the database then assign them as choices
        class_section_choices = [(obj.section_name, obj.section_name) for obj in ClassSection.objects.all().order_by('grade_level')]
        teachers = Teacher.objects.all()
        teacher_choices = [(teacher.user.id, f"{teacher.user.first_name} {teacher.user.last_name}") for teacher in teachers]

        self.fields['teacher'].choices = teacher_choices

        self.fields['grade_level'].choices = grade_level_choices
        self.fields['grade_level'].widget.attrs['class'] = 'form-select'
        self.fields['grade_level'].widget.attrs['required'] = 'required'

        self.fields['class_section'].choices = class_section_choices
        self.fields['class_section'].widget.attrs['class'] = 'form-select'
        self.fields['class_section'].widget.attrs['required'] = 'required'

    @transaction.atomic # Package the database operation to maintain data integrity.
    def save(self):
        # Save the Student account into the User model
        user = super().save(commit=False)
        username = self.generate_unqiue_username(
            user.first_name,
            user.last_name,
            self.cleaned_data['grade_level'],
            self.cleaned_data['class_section'][:3]
        )
        user.username = username
        user.is_student = True
        user.save()

        # Create a Student model associated with the Student User Account
        # And add the necessary data into their respective fields
        student = Student.objects.create(user=user)
        student.grade_level = self.cleaned_data['grade_level']
        student.class_section = self.cleaned_data['class_section']
        student.save()

    # Override clean methods to convert to Title Case / Capital first letter
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capwords(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capwords(last_name)
    
    def generate_unique_username(self, first_name, last_name, grade_level, section):
        first_name = first_name.lower()
        last_name = last_name.lower()

        # Generate a unique username based on first name, last name, grade level, and section
        username = slugify(f"{first_name}.{last_name}-{grade_level}{section}")
        
        # Check if the username already exists
        while User.objects.filter(username=username).exists():
            # If it exists, append a random string to make it unique
            random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
            username += f"-{random_string}"
        
        return username


class CustomPasswordResetConfirmForm(SetPasswordForm):
    # This is a custom form where the user types their new password
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetConfirmForm, self).__init__(*args, **kwargs)

        # Customize widget attributes for password inputs
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = '' 
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>' 

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'  
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	