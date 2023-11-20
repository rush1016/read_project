from django.shortcuts import get_object_or_404

from materials.models import Passage
from assessment.models import AssessmentSessionPassage


def update_assessment_passage_data(passage_id, assessment_instance, score, reading_time, answering_time):
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    assessment_passage = get_object_or_404(AssessmentSessionPassage, assessment_session=assessment_instance, passage=passage_instance)
    
    assessment_passage.score = score
    
    if assessment_passage.reading_time:
        assessment_passage.reading_time += int(reading_time)
    else:
        assessment_passage.reading_time = reading_time

    if assessment_passage.answering_time:
        assessment_passage.answering_time += int(answering_time)
    else: 
        assessment_passage.answering_time = answering_time

    assessment_passage.save()