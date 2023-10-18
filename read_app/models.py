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
    )
    teacher_code = models.CharField(max_length=80)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='student_profile'
    )
    teacher = models.ForeignKey(
        'read_app.User', 
        on_delete=models.SET_NULL, 
        null=True,
    )
    student_id = models.IntegerField(unique=True)
    student_lrn = models.FloatField(unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_added = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    # Assessments
    has_ongoing_assessment = models.BooleanField(default=False)
    overall_rating = models.CharField(default=0, max_length=100)
    words_per_minute = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    mean_read_time = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    mean_score = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    assessments_done = models.IntegerField(default=0)
    fourth_grade_passage = models.IntegerField(default=0)
    fifth_grade_passage = models.IntegerField(default=0)
    sixth_grade_passage = models.IntegerField(default=0)


class ArchivedStudent(models.Model):
    previous_teacher = models.ForeignKey(
        'read_app.User', 
        on_delete=models.SET_NULL, 
        null=True
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    student_id = models.IntegerField()
    student_lrn = models.FloatField(unique=True, null=True)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_added = models.DateField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    date_archived = models.DateField(auto_now_add=True)


class ClassSection(models.Model):
    grade_level = models.IntegerField()
    section_name = models.CharField(max_length=80)


class Passage(models.Model):
    passage_title = models.CharField(max_length=150)
    passage_content = models.CharField(max_length=5000)
    grade_level = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.passage_title


class Question(models.Model):
    passage = models.ForeignKey(
        'read_app.Passage', on_delete=models.CASCADE
    )
    question_content = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question_content


class Choice(models.Model):
    question = models.ForeignKey(
        'read_app.Question', on_delete=models.CASCADE
    )
    choice_content = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_content


class StudentAnswer(models.Model):
    student = models.ForeignKey(
        'read_app.Student', on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'read_app.Question', on_delete=models.CASCADE
    )
    answer_content = models.CharField(max_length=500)


class AssessmentSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    ASSESSMENT_TYPES = (
        ('Screening', 'Screening'),
        ('Normal', 'Normal'),
    )
    assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_TYPES)
    grade_level = models.IntegerField()
    total_score = models.IntegerField(null=True)
    total_reading_time = models.PositiveIntegerField(null=True)
    total_answering_time = models.PositiveIntegerField(null=True)
    assigned_time = models.DateTimeField(default=timezone.now)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Assessment Session for {self.student}"
    

class AssessmentSessionPassage(models.Model):
    assessment_session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)