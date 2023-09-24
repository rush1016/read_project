from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
class Admin(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    password = models.CharField(max_length=80)
    date_created = models.DateField(default=datetime.date.today)


class Teacher(AbstractUser):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_created = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class Student(models.Model):
    teacher = models.ForeignKey(
        'read_app.Teacher', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    grade_level = models.IntegerField()
    date_added = models.DateField(default=datetime.date.today)


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