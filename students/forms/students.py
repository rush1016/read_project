from django import forms
from django.core.validators import RegexValidator
from string import capwords

from students.models import Student, ClassSection


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'first_name', 
            'middle_name',
            'last_name', 
            'suffix',
            'age',
            'grade_level', 
            'class_section',
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
    grade_level = forms.ChoiceField(
        choices=[], 
        label='Grade Level',
    )
    class_section = forms.ChoiceField(
        choices=[], 
        label='Section',
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


    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
        GRADE_LEVEL_CHOICES = [
            (4, 'Grade 4'),
            (5, 'Grade 5'),
            (6, 'Grade 6'),
        ]
        # Get the class section data from the database then assign them as choices
        CLASS_SECTION_CHOICES = [(obj.section_name, obj.section_name) for obj in ClassSection.objects.all().order_by('grade_level')]

        self.fields['grade_level'].choices = GRADE_LEVEL_CHOICES
        self.fields['grade_level'].widget.attrs['class'] = 'form-select'
        self.fields['grade_level'].widget.attrs['required'] = 'required'

        self.fields['class_section'].choices = CLASS_SECTION_CHOICES
        self.fields['class_section'].widget.attrs['class'] = 'form-select'
        self.fields['class_section'].widget.attrs['required'] = 'required'