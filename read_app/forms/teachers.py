from django.db import transaction
from read_app.models import Teacher
from .base_registration import BaseRegistrationForm
import string
import random


class TeacherRegistrationForm(BaseRegistrationForm):
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

        # Create a Student model associated with the Student User Account
        # And add the necessary data into their respective fields
        teacher = Teacher.objects.create(user=user)
        teacher.teacher_code = self.generate_registration_code()
        teacher.save()

    def generate_registration_code(self):
        # Define the length of the registration code
        code_length = 6  # You can adjust the length as needed

        # Generate a random code consisting of letters and digits
        characters = string.ascii_letters + string.digits
        registration_code = ''.join(random.choice(characters) for _ in range(code_length))

        return registration_code