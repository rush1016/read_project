def calculate_screening_rating(student_instance, assessment_instance):
    # Check if it's a Screening Assessment and the student has passed the screening test
    if assessment_instance.assessment_type == 'Screening':
        if assessment_instance.total_score >= 14:
            overall_rating = 'Passed Screening Test'
        else:
            overall_rating = 'Further Assessment Required'

        # Update the student's overall_rating
        student_instance.overall_rating = overall_rating
        student_instance.is_screened= True
        student_instance.save()