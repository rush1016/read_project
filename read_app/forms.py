from django.contrib.auth.forms import UserCreationForm, SetPasswordForm,password_validation
from django.core.validators import RegexValidator
from django import forms
from .models import Teacher, Student, ClassSection
from string import capwords


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Email Address'}))
    first_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'First Name'}))
    last_name = forms.CharField(
        label="", 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class':'form-control', 
                'placeholder':'Last Name'}))

    class Meta:
        model = Teacher 
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	


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


class StudentForm(forms.ModelForm):
    # Regular expression pattern for valid names
    name_validator = RegexValidator(
        regex=r'^[A-Za-z\s\'-]+$',
        message='Enter a valid name containing only letters, spaces, hyphens, and apostrophes.',
    )
    # Apply the validator for both first_name and last_name
    first_name = forms.CharField(
        validators=[name_validator],  
        label='First Name',
    )
    last_name = forms.CharField(
        validators=[name_validator],  
        label='Last Name',
    )
    grade_level = forms.ChoiceField(choices=[], label='Grade Level')
    class_section = forms.ChoiceField(choices=[], label='Section')

    # Override clean methods to convert to Title Case / Capital first letter
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capwords(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capwords(last_name)

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grade_level', 'class_section']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        grade_level_choices = [
            (4, 'Grade 4'),
            (5, 'Grade 5'),
            (6, 'Grade 6'),
        ]
        class_section_choices = [(obj.section_name, obj.section_name) for obj in ClassSection.objects.all()]

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'

        self.fields['grade_level'].choices = grade_level_choices
        self.fields['grade_level'].widget.attrs['class'] = 'form-select'
        self.fields['grade_level'].widget.attrs['required'] = 'required'

        self.fields['class_section'].choices = class_section_choices
        self.fields['class_section'].widget.attrs['class'] = 'form-select'
        self.fields['class_section'].widget.attrs['required'] = 'required'