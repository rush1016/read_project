from django.db import models
from materials.models import Passage
from django.utils import timezone

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
    total_score = models.IntegerField(null=True)
    total_reading_time = models.PositiveIntegerField(null=True)
    total_answering_time = models.PositiveIntegerField(null=True)
    assigned_time = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Assessment Session for {self.student}"
    
    def get_passages(self):
        return self.assessment_passage.all()

    def get_responses(self):
        return self.student_answer.all()
    

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

    def __str__(self):
        return f'Graded Assessment for {self.assessment_session.student}'


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