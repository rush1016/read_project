from django.db import models
from django.utils import timezone

from read_app.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='student_instance',
        limit_choices_to={
            'is_student': True
        },
    )
    teacher = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={
            'is_teacher': True
        },
    )
    student_id = models.IntegerField(unique=True)
    student_school_id = models.CharField(unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_added = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    # Assessments
    is_screened = models.BooleanField(default=False)
    screening = models.BooleanField(default=False)
    overall_rating = models.CharField(default=0, max_length=100)
    words_per_minute = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    mean_read_time = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    mean_score = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    assessments_done = models.IntegerField(default=0)
    fourth_grade_passage = models.IntegerField(default=0)
    fifth_grade_passage = models.IntegerField(default=0)
    sixth_grade_passage = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        has_screening_session = self.assessment_session.filter(
            assessment_type = 'Screening'
        ).exists()
        print(has_screening_session)

        self.screening = has_screening_session
        super().save(*args, **kwargs)



class ArchivedStudent(models.Model):
    previous_teacher = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    student_id = models.IntegerField()
    student_school_id = models.CharField(unique=True, null=True)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_added = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    date_archived = models.DateField(auto_now_add=True)


class ClassSection(models.Model):
    grade_level = models.IntegerField()
    section_name = models.CharField(max_length=80)