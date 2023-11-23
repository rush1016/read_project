from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


class School(models.Model):
    school_code = models.PositiveBigIntegerField()
    registration_code = models.CharField()
    name = models.CharField(max_length=64)
    division = models.CharField(max_length=64)
    district = models.CharField(max_length=64)
    region = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade_level = models.IntegerField()
    grade_name = models.CharField()

    def __str__(self):
        return self.grade_name

class ClassSection(models.Model):
    grade_level = models.IntegerField()
    section_name = models.CharField(max_length=80)

    def __str__(self):
        return self.section_name

class User(AbstractUser):
    is_teacher = models.BooleanField('Teacher status', default=False)
    is_school_admin = models.BooleanField('School Admin status', default=False)

    def __str__(self):
        return self.get_full_name()
    

class Admin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='school_admin',
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school"
    )
    date_created = models.DateField(default=timezone.now)


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'is_teacher': True},
        related_name='teacher'
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    GRADE_LEVELS = ((grade.grade_level, grade.grade_name) for grade in Grade.objects.all())
    CLASS_SECTIONS = ((section.section_name, section.section_name) for section in ClassSection.objects.all())
    grade_level = models.IntegerField(choices=GRADE_LEVELS)
    section = models.CharField(choices=CLASS_SECTIONS)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()

