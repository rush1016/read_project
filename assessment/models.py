from django.db import models
from materials.models import Passage
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from students.models import Student
from materials.models import Question, Choice

class AssessmentSession(models.Model):
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='assessment_session',
    )
    ASSESSMENT_TYPES = (
        ('Screening', 'Screening'),
        ('Graded', 'Graded'),
    )
    assessment_type = models.CharField(max_length=16, choices=ASSESSMENT_TYPES)
    number_of_questions = models.IntegerField(default=0)
    grade_level = models.IntegerField()
    total_score = models.IntegerField(null=True, blank=True)
    total_reading_time = models.PositiveIntegerField(null=True, blank=True)
    total_answering_time = models.PositiveIntegerField(null=True, blank=True)

    assigned_time = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    passcode = models.CharField(max_length=16, unique=True)
    
    def __str__(self):
        return f"Assessment Session for {self.student}"
    
    def get_passages(self):
        return self.assessment_passage.all()
    
    def get_graded_passage(self):
        return self.assessment_passage.all().first()

    def get_responses(self):
        return self.student_answer.all()
    
    def get_miscues(self):
        return self.oral_miscues.all()


# Signal to update assessments_done when a new AssessmentSession is created
@receiver(post_save, sender=AssessmentSession)
def update_assessments_done(sender, instance, **kwargs):
    if instance.is_finished:
        instance.student.assessments_done = instance.student.assessment_session.filter(assessment_type='Graded', is_finished=True).count()
        instance.student.save()


class AssessmentMiscue(models.Model):
    assessment = models.ForeignKey(
        AssessmentSession,
        on_delete=models.CASCADE,
        related_name="oral_miscues",
    )
    passage = models.ForeignKey(
        Passage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    word = models.CharField(max_length=64)
    MISCUE_TYPES = (
        ('Mispronunciation', 'Mispronunciation'),
        ('Omission', 'Omission'),
        ('Substitution', 'Substitution'),
        ('Insertion', 'Insertion'),
        ('Repetition', 'Repetition'),
        ('Transposition', 'Transposition'),
        ('Reversal', 'Reversal'),
        ('Self-correction', 'Self-correction'),
    )
    miscue = models.CharField(choices=MISCUE_TYPES)
    index = models.IntegerField()
    

class ScreeningAssessment(models.Model):
    assessment_session = models.OneToOneField(
        AssessmentSession,
        on_delete=models.CASCADE,
        related_name='screening_assessment'
    )
    current_passage = models.IntegerField(default=1)

    correct_literal = models.PositiveIntegerField(default=0)
    correct_inferential = models.PositiveIntegerField(default=0)
    correct_critical = models.PositiveIntegerField(default=0)

    total_literal = models.PositiveIntegerField(default=0)
    total_inferential = models.PositiveIntegerField(default=0)
    total_critical = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'Screening Test for {self.assessment_session.student}'
    
    def update_question_counts(self):
        # Iterate through related passages and their questions
        for assessment_passage in self.assessment_session.get_passages():
            questions = assessment_passage.passage.get_questions()
            for question in questions:
                if question.question_type == 'Literal':
                    self.total_literal += 1
                elif question.question_type == 'Inferential':
                    self.total_inferential += 1
                elif question.question_type == 'Critical':
                    self.total_critical += 1

        # Save the updated counts
        self.save()

class GradedAssessment(models.Model):
    assessment_session = models.OneToOneField(
        AssessmentSession,
        on_delete=models.CASCADE,
        related_name='graded_assessment'
    )
    RATINGS = (
        ("Independent", "Independent"),
        ("Instructional", "Instructional"),
        ("Frustration", "Frustration"),
    )

    def __str__(self):
        return f'Graded Assessment for {self.assessment_session.student}'
    
    oral_reading_score = models.FloatField(null=True, blank=True)
    reading_comprehension_score = models.FloatField(null=True, blank=True)

    oral_reading_rating = models.CharField(null=True, blank=True, choices=RATINGS)
    reading_comprehension_rating = models.CharField(null=True, blank=True, choices=RATINGS)

    overall_rating = models.CharField(null=True, blank=True, choices=RATINGS)

    reading_speed = models.FloatField(null=True, blank=True)



class AssessmentSessionPassage(models.Model):
    assessment_session = models.ForeignKey(
        AssessmentSession, 
        on_delete=models.CASCADE, 
        related_name='assessment_passage'
    )
    order = models.PositiveIntegerField(null=True)
    passage = models.ForeignKey(
        Passage, 
        on_delete=models.CASCADE,
        related_name='assessment_passage',
    )
    score = models.PositiveIntegerField(null=True, blank=True)
    reading_time = models.PositiveIntegerField(null=True, blank=True)
    answering_time = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.passage.passage_title


class StudentAnswer(models.Model):
    assessment = models.ForeignKey(
        AssessmentSession, on_delete=models.CASCADE, related_name="student_answer"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE
    )
    passage = models.ForeignKey(
        Passage, on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        Choice, on_delete=models.SET_NULL, null=True
    )
    correct = models.BooleanField(default=False)

    def __string__(self):
        return f'Answer of {self.student}'