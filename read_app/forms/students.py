from django import forms
from .base_registration import BaseRegistrationForm
from django.db import transaction
from ..models import User, Teacher, Student, ClassSection

# For unique username generator
from django.utils.text import slugify

class StudentRegistrationForm(BaseRegistrationForm):
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
                'required': 'required',}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'teacher', 'grade_level', 'class_section', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)
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
        username = self.generate_unique_username(
            user.first_name,
            user.last_name,
            self.cleaned_data['grade_level'],
            self.cleaned_data['class_section'][:3]
        )
        user.username = username
        user.is_student = True
        user.save()

        # Create an instance of corresponding teacher and assign it as foreign key
        teacher_user_id = self.cleaned_data['teacher']
        teachers = Teacher.objects.get(pk=teacher_user_id)
        # Create a Student model associated with the Student User Account
        # And add the necessary data into their respective fields
        student = Student.objects.create(
            user=user,
            teacher=teachers,
            grade_level=self.cleaned_data['grade_level'], 
            class_section=self.cleaned_data['class_section']
        )

        student.save()

    def generate_unique_username(self, first_name, last_name, grade_level, section):
        first_name = first_name.lower()
        last_name = last_name.lower()

        # Generate a unique username based on first name, last name, grade level, and section
        base_username = slugify(f"{first_name}.{last_name}-{grade_level}{section}")
        
        if not User.objects.filter(username=base_username).exists():
                return base_username

        # If the base username exists, find the next available incrementing number
        i = 1
        while True:
            username = f"{base_username}-{i}"
            if not User.objects.filter(username=username).exists():
                return username
            i += 1