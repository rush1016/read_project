from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError

from read_app.forms.base_registration import BaseRegistrationForm
from read_app.models import User, Teacher
from students.models import Student, ClassSection

# For unique username generator
from django.utils.text import slugify

class StudentRegistrationForm(BaseRegistrationForm):
    class Meta:
        model = User
        fields = (
             'teacher_code', 
             'first_name', 
             'last_name', 
             'grade_level', 
             'class_section', 
             'email', 
             'password1', 
             'password2')

    grade_level = forms.ChoiceField(
        choices=[], 
        label='Grade Level',
    )
    class_section = forms.ChoiceField(
        choices=[], 
        label='Section',
    )
    teacher_code = forms.CharField(
        label='Teacher Code',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Teacher Registration Code',
                'required': 'required',}))

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
    
    def clean_teacher_code(self):
         cleaned_data = super().clean()
         teacher_code = cleaned_data.get('teacher_code')

         teacher_exists = Teacher.objects.filter(teacher_code=teacher_code)

         if not teacher_exists:
              raise ValidationError("Invalid teacher code. Please enter ask your Teacher for their registration code.")
         
         return teacher_code

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
        teacher_code = self.cleaned_data['teacher_code']
        teacher_instance = Teacher.objects.get(teacher_code=teacher_code)
        teacher_user_instance = User.objects.get(pk=teacher_instance.user.id)

        # Assign the student info into the Student model too
        student_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        grade_level = self.cleaned_data['grade_level']
        class_section = self.cleaned_data['class_section']

        # Create a Student model associated with the Student User Account
        # And add the necessary data into their respective fields
        student = Student.objects.create(
            user=user,                      # Primary Key (Instance)
            teacher=teacher_user_instance,  # Foreign Key (Instance)
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            grade_level=grade_level, 
            class_section=class_section
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
