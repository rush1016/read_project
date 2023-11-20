from django.db import models
from django.utils import timezone


class AssessmentPreset(models.Model):
    ASSESSMENT_TYPES = (
        ('Screening', 'Screening'),
        ('Graded', 'Graded'),
    )
    LANGUAGES = (
        ('English', 'English'),
        ('Filipino', 'Filipino'),
    )
    grade_level = models.IntegerField()
    assessment_type = models.CharField(max_length=16, choices=ASSESSMENT_TYPES)
    language = models.CharField(choices=LANGUAGES)
    name = models.CharField(max_length=127)

    def __str__(self):
        return f'{self.name}'


class Passage(models.Model):
    preset = models.ForeignKey(
        AssessmentPreset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    LANGUAGES = (
        ('Filipino', 'Filipino'),
        ('English', 'English'),
    )
    language = models.CharField(choices=LANGUAGES)
    SETS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    )
    set = models.CharField(null=True, blank=True, choices=SETS)
    passage_title = models.CharField(max_length=150)
    passage_content = models.CharField(max_length=5000)
    grade_level = models.IntegerField()
    passage_length = models.IntegerField()
    number_of_questions = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.passage_title
    
    def save(self, *args, **kwargs):
        # Calculate and update passage length before saving
        self.passage_length = len(self.passage_content.split())
        super(Passage, self).save(*args, **kwargs)

    def get_questions(self):
        return self.question_set.all()


class Question(models.Model):
    passage = models.ForeignKey(
        Passage, on_delete=models.CASCADE
    )
    QUESTION_TYPES = (
        ('Literal', 'Literal'),
        ('Inferential', 'Inferential'),
        ('Critical', 'Critical'),
    )
    question_type = models.CharField(max_length=64, choices=QUESTION_TYPES, null=True, blank=True)
    question_content = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question_content
    
    def get_choices(self):
        return self.choice_set.all()
    
    def get_correct(self):
        return self.choice_set.get(is_correct=True)


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    choice_content = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_content
    
    def get_content(self):
        return self.choice_content