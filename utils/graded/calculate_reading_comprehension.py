def calculate_reading_comprehension(assessment_instance):
    assessment = assessment_instance
    graded_assessment = assessment_instance.graded_assessment
    total_score = assessment.total_score
    question_count = assessment.number_of_questions

    reading_comprehension_score = (total_score/question_count)*100

    # Calculate reading comprehension score
    if 80 <= reading_comprehension_score <= 100:
        rating = 'Independent'
    elif 59 <= reading_comprehension_score <= 79:
        rating = 'Instructional'
    elif reading_comprehension_score <= 58:
        rating = 'Frustration'

    # Calculate Overall Rating based on Oral Reading Rating and Comprehension Rating
    graded_assessment.reading_comprehension_score = reading_comprehension_score
    graded_assessment.reading_comprehension_rating = rating
    graded_assessment.save()