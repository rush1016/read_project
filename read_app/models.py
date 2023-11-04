from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import datetime


class User(AbstractUser):
    is_student = models.BooleanField('Student status', default=False)
    is_teacher = models.BooleanField('Teacher status', default=False)
    is_school_admin = models.BooleanField('School Admin status', default=False)

    def __str__(self):
        return self.get_full_name()
    

class Admin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_created = models.DateField(default=timezone.now)


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'is_teacher': True},
    )
    teacher_code = models.CharField(max_length=80)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()