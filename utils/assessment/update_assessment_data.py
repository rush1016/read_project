from django.db import models
from django.utils import timezone

def update_assessment_data(assessment_instance, extra_reading_time, review_count):
    extra_reading_time = int(extra_reading_time)
    # Summ all the total values of score, reading time, and answering time
    assessment_instance.total_score = assessment_instance.assessment_passage.aggregate(total_score=models.Sum('score'))['total_score'] or 0
    assessment_instance.total_reading_time = assessment_instance.assessment_passage.aggregate(total_reading_time=models.Sum('reading_time'))['total_reading_time'] or 0
    assessment_instance.total_answering_time = assessment_instance.assessment_passage.aggregate(total_answering_time=models.Sum('answering_time'))['total_answering_time'] or 0

    # The modal for displaying the story after student clicked the start
    # answering button. Counted as extra reading time and added into the
    # total reading time. The amount of times the student viewed the modal
    # is also counted.
    if assessment_instance.extra_reading_time:
        assessment_instance.extra_reading_time += extra_reading_time
    else:
        assessment_instance.extra_reading_time = extra_reading_time

    assessment_instance.total_reading_time += extra_reading_time
    assessment_instance.review_count = review_count
    assessment_instance.end_time = timezone.now()
    if assessment_instance.assessment_type == 'Graded':
        assessment_instance.is_finished = True

    assessment_instance.save()