def calculate_oral_reading(assessment_instance):
    assessment = assessment_instance
    passage = assessment.get_passages()[0].passage # Get the first and only passage
    graded_assessment = assessment_instance.graded_assessment

    miscues_count = assessment.get_miscues().count()
    word_count = passage.passage_length

    oral_reading_score = ((word_count-miscues_count)/word_count)*100

    if 97 <= oral_reading_score <= 100:
        rating = 'Independent'
    elif 90 <= oral_reading_score <= 96:
        rating = 'Instructional'
    else:
        rating = 'Frustration'

    graded_assessment.oral_reading_score = oral_reading_score
    graded_assessment.oral_reading_rating = rating
    graded_assessment.save()