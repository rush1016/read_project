from django.shortcuts import get_object_or_404

from assessment.models import AssessmentSessionPassage


def update_assessment_passage_data(passage_instance, assessment_instance, score, reading_time, answering_time):
    assessment_passage = get_object_or_404(AssessmentSessionPassage, assessment_session=assessment_instance, passage=passage_instance)
    reading_time = int(reading_time)
    if reading_time == 0:
        reading_time += 1
    answering_time = int(answering_time)
    word_count = int(passage_instance.passage_length)
    words_per_minute = (word_count/reading_time)*60
    

    assessment_passage.score = score
    if assessment_passage.reading_time:
        assessment_passage.reading_time += reading_time
    else:
        assessment_passage.reading_time = reading_time

    if assessment_passage.answering_time:
        assessment_passage.answering_time += answering_time
    else: 
        assessment_passage.answering_time = answering_time
    assessment_passage.words_per_minute = words_per_minute

    assessment_passage.save()