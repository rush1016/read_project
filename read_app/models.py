from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    is_student = models.BooleanField('student_status', default=False)
    is_teacher = models.BooleanField('teacher_status', default=False)
    is_school_admin = models.BooleanField('school_admin_status', default=False)


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
        'read_app.Teacher', 
        on_delete=models.SET_NULL, 
        null=True, 
        )
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
    class_section = models.CharField(max_length=80, default='undefined')
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
    passage_grade = models.IntegerField()


class PassageQuestion(models.Model):
    passage = models.ForeignKey(
        'read_app.Passage', on_delete=models.CASCADE
    )
    question_content = models.CharField(max_length=500)
    question_type = models.CharField(max_length=50)


class MultipleChoice(models.Model):
    question = models.ForeignKey(
        'read_app.PassageQuestion', on_delete=models.CASCADE
    )
    choice_label = models.CharField(max_length=10)
    choice_content = models.CharField(max_length=500)
    is_correct = models.BooleanField()


class TrueFalse(models.Model):
    question = models.ForeignKey(
        'read_app.PassageQuestion', on_delete=models.CASCADE
    )
    choice_content = models.CharField(max_length=500)
    is_correct = models.BooleanField()


class FillBlanks(models.Model):
    question = models.ForeignKey(
        'read_app.PassageQuestion', on_delete=models.CASCADE
    )
    answer_content = models.CharField(max_length=500)


class OpenEnded(models.Model):
    question = models.ForeignKey(
        'read_app.PassageQuestion', on_delete=models.CASCADE
    )
    answer_content = models.CharField(max_length=500)


class StudentAnswer(models.Model):
    student = models.ForeignKey(
        'read_app.Student', on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'read_app.PassageQuestion', on_delete=models.CASCADE
    )
    answer_content = models.CharField(max_length=500)


class AssessmentInfo(models.Model):
    student = models.ForeignKey(
        'read_app.Student', on_delete=models.CASCADE
    )
    first_passage = models.IntegerField()
    second_passage = models.IntegerField()
    third_passage = models.IntegerField()
    fourth_passage = models.IntegerField()
    read_time = models.TimeField(default=None)
    answer_time = models.TimeField(default=None)
    score = models.IntegerField()
    date_started = models.DateTimeField(null=True, blank=True)
    date_finished = models.DateTimeField(null=True, blank=True)
