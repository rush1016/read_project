def calculate_overall_rating(student_instance, assessment_instance):
    # Check if it's a Screening Assessment and the student has passed the screening test
    if assessment_instance.assessment_type == 'Screening':
        if assessment_instance.total_score >= 14:
            overall_rating = 'Passed Screening Test'
        else:
            overall_rating = 'Further Assessment Required'

    else:
        # Calculate the percentage of total_score
        total_score = assessment_instance.total_score
        question_count = assessment_instance.number_of_questions
        if total_score is not None:
            percentage = (total_score / question_count) * 100
        else:
            percentage = 0  # Handle the case when total_score is None or not set
        print('percentage: ', percentage)
        # Determine the RATING based on the percentage
        if percentage >= 80:
            overall_rating = 'Independent'
        elif percentage >= 59:
            overall_rating = 'Instructional'
        else:
            overall_rating = 'Frustration'

    # Update the student's overall_rating
    student_instance.overall_rating = overall_rating
    student_instance.save()