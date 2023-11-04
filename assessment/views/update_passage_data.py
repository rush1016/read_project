from django.shortcuts import get_object_or_404

from materials.models import Passage
from assessment.models import AssessmentSessionPassage


def update_assessment_passage_data(passage_id, assessment_instance, score, reading_time, answering_time):
    passage_instance = get_object_or_404(Passage, pk=passage_id)
    assessment_passage = get_object_or_404(AssessmentSessionPassage, assessment_session=assessment_instance, passage=passage_instance)
    assessment_passage.score = score
    assessment_passage.reading_time = reading_time
    assessment_passage.answering_time = answering_time
    assessment_passage.save()