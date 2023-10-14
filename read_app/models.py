from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import datetime


class User(AbstractUser):
    is_student = models.BooleanField('student_status', default=False)
    is_teacher = models.BooleanField('teacher_status', default=False)
    is_school_admin = models.BooleanField('school_admin_status', default=False)

    def __str__(self):
        return self.get_full_name()


class Admin(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_created = models.DateField(default=datetime.date.today)


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    teacher_code = models.CharField(max_length=80)
    date_created = models.DateField(default=datetime.date.today)

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
    date_added = models.DateField(default=datetime.date.today)
    is_archived = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class ArchivedStudent(models.Model):
    teacher = models.ForeignKey('read_app.Teacher', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_archived = models.DateField(auto_now_add=True)


class ClassSection(models.Model):
    grade_level = models.IntegerField()
    section_name = models.CharField(max_length=80)


class StudentInfo(models.Model):
    student = models.ForeignKey(
        'read_app.Student', on_delete=models.CASCADE
    )
    overall_rating = models.CharField(max_length=100)
    words_per_minute = models.DecimalField(decimal_places=2, max_digits=10)
    mean_read_time = models.DecimalField(decimal_places=2, max_digits=10)
    mean_score = models.DecimalField(decimal_places=2, max_digits=10)
    assessments_done = models.IntegerField()
    fourth_grade_passage = models.IntegerField()
    fifth_grade_passage = models.IntegerField()
    sixth_grade_passage = models.IntegerField()


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
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    total_reading_time = models.PositiveIntegerField()
    total_answering_time = models.PositiveIntegerField()
    grade_level = models.IntegerField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Assessment Session for {self.student} - Passage: {self.passage.passage_title}"