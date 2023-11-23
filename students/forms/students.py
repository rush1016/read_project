from django import forms
from django.core.validators import RegexValidator
from string import capwords

from students.models import Student
from read_app.models import Grade, ClassSection


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'first_name', 
            'middle_name',
            'last_name', 
            'suffix',
            'age',
        )
    SUFFIXES = (
        ('', 'No suffix'),
        ('Sr.', 'Sr.'),
        ('Jr.', 'Jr.'),
        ('III', 'III'),
    )

    first_name = forms.CharField(
        label = 'First Name',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter First Name',
            }
        ),
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid first name containing only letters, spaces, hyphens, and apostrophes.',)]
    )
    middle_name = forms.CharField(
        label='Middle Name',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Middle Name (Optional)',
            }
        ),
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid middle name containing only letters, spaces, hyphens, and apostrophes.',)],
        required=False
    )
    last_name = forms.CharField(
        label='Last Name',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Last Name',
            }
        ),
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid last name containing only letters, spaces, hyphens, and apostrophes.',)]
    )
    suffix = forms.ChoiceField(
        label='Suffix',
        choices=SUFFIXES,
        widget = forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        required=False
    )
    age = forms.IntegerField(
        label='Age',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter age of student'
            }
        )
    )

    # Override clean methods to convert to Title Case / Capital first letter
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return capwords(first_name)

    def clean_middle_name(self):
        middle_name = self.cleaned_data['middle_name']
        return capwords(middle_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return capwords(last_name)

    def save(self, teacher):
        student = super().save(commit=False)


        student.teacher = teacher.user
        student.school = teacher.school
        student.grade_level = teacher.grade_level
        student.class_section = teacher.section

        student.save()
        
        return student