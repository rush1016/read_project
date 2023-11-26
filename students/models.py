from django.db import models
from django.utils import timezone

from read_app.models import User, School


class Student(models.Model):
    teacher = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        limit_choices_to={
            'is_teacher': True
        },
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(null=True, blank=True)
    last_name = models.CharField(max_length=80)
    SUFFIXES = (
        ('Sr.', 'Sr.'),
        ('Jr.', 'Jr.'),
        ('III', 'III'),
    )

    suffix = models.CharField(choices=SUFFIXES, null=True, blank=True)

    age = models.PositiveIntegerField(null=True, blank=True)
    grade_level = models.IntegerField()
    class_section = models.CharField(max_length=80)
    date_added = models.DateField(default=timezone.now)

    # Assessments
    RATING = (
        ('Independent', 'Independent'),
        ('Instructional', 'Instructional'),
        ('Frustration', 'Frustration'),
        ('Passed Screening Test', 'Passed Screening Test'),
        ('Further Assessment Required', 'Further Assessment Required'),
        ('Not yet screened', 'Not yet screened'),
    )

    is_screened = models.BooleanField(default=False)
    screening = models.BooleanField(default=False)
    gst_score = models.PositiveIntegerField(null=True, blank=True)
    recommended_grade_level = models.PositiveIntegerField(default=0)
    overall_rating = models.CharField(default='Not yet screened', max_length=64)

    mean_read_time = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    mean_score = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    assessments_done = models.IntegerField(default=0)

    first_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    second_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    third_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    fourth_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    fifth_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    sixth_grade_rating = models.CharField(null=True, blank=True, choices=RATING)
    seventh_grade_rating = models.CharField(null=True, blank=True, choices=RATING)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_name(self):
        full_name = f'{self.last_name}, {self.first_name}'
        if self.middle_name:
            full_name += f' {self.middle_name[:1]}.' 
        
        if self.suffix:
            full_name += f' {self.suffix}'
        
        return full_name
    
    def get_assessments(self):
        return self.assessment_session.all()
    
    def get_screening(self):
        return self.assessment_session.filter(assessment_type="Screening").order_by('-assigned_time')
    
    def get_graded(self):
        return self.assessment_session.filter(assessment_type="Graded").order_by('-assigned_time')

    def save(self, *args, **kwargs):
        # Set recommended_grade_level to the value of grade_level if not explicitly set
        if not self.recommended_grade_level:
            self.recommended_grade_level = self.grade_level

        super().save(*args, **kwargs)


class StudentRating(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="student_rating"
    )
    RATING = (
        ('Independent', 'Independent'),
        ('Instructional', 'Instructional'),
        ('Frustration', 'Frustration'),
    )

    english_rating = models.CharField(null=True, blank=True)
    english_recommended_grade = models.IntegerField(null=True, blank=True)
    english_gst_score = models.PositiveIntegerField(null=True, blank=True)

    filipino_rating = models.CharField(null=True, blank=True)
    filipino_recommended_grade = models.IntegerField(null=True, blank=True)
    filipino_gst_score = models.PositiveIntegerField(null=True, blank=True)

    first_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    second_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    third_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    fourth_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    fifth_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    sixth_grade_eng = models.CharField(choices=RATING, null=True, blank=True)
    seventh_grade_eng = models.CharField(choices=RATING, null=True, blank=True)

    first_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    second_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    third_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    fourth_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    fifth_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    sixth_grade_fil = models.CharField(choices=RATING, null=True, blank=True)
    seventh_grade_fil = models.CharField(choices=RATING, null=True, blank=True)

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

