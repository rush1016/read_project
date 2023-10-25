from django import forms
from django.core.validators import RegexValidator

from students.models import Student, ClassSection


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_lrn', 'first_name', 'last_name', 'grade_level', 'class_section']

    first_name = forms.CharField(
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'First Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid first name containing only letters, spaces, hyphens, and apostrophes.',)])
    last_name = forms.CharField(
        max_length=80, 
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'Last Name'}),
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z\s\'-]+$',
                'Enter a valid last name containing only letters, spaces, hyphens, and apostrophes.',)])
    grade_level = forms.ChoiceField(
        choices=[], 
        label='Grade Level',
    )
    class_section = forms.ChoiceField(
        choices=[], 
        label='Section',
    )
    student_lrn = forms.FloatField(
        label='Student LRN',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Student's LRN",
        })
    )

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        grade_level_choices = [
            (4, 'Grade 4'),
            (5, 'Grade 5'),
            (6, 'Grade 6'),
        ]
        # Get the class section data from the database then assign them as choices
        class_section_choices = [(obj.section_name, obj.section_name) for obj in ClassSection.objects.all().order_by('grade_level')]

        self.fields['grade_level'].choices = grade_level_choices
        self.fields['grade_level'].widget.attrs['class'] = 'form-select'
        self.fields['grade_level'].widget.attrs['required'] = 'required'

        self.fields['class_section'].choices = class_section_choices
        self.fields['class_section'].widget.attrs['class'] = 'form-select'
        self.fields['class_section'].widget.attrs['required'] = 'required'