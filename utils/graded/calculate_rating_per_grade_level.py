def calculate_rating_per_grade_level(assessment_instance):
    assessment_grade_level = assessment_instance.grade_level
    overall_rating = assessment_instance.graded_assessment.overall_rating
    student = assessment_instance.student

    if assessment_grade_level == 1:
        student.first_grade_rating = overall_rating
    elif assessment_grade_level == 2:
        student.second_grade_rating = overall_rating
    elif assessment_grade_level == 3:
        student.third_grade_rating = overall_rating
    elif assessment_grade_level == 4:
        student.fourth_grade_rating = overall_rating
    elif assessment_grade_level == 5:
        student.fifth_grade_rating = overall_rating
    elif assessment_grade_level == 6:
        student.sixth_grade_rating = overall_rating
    elif assessment_grade_level == 7:
        student.seventh_grade_rating = overall_rating

    student.save()