def calculate_student_overall_rating(assessment_instance):
    graded_assessment = assessment_instance.graded_assessment
    passage = assessment_instance.get_passages()[0]
    student_instance = assessment_instance.student

    assessment_grade_level = passage.passage.grade_level
    assessment_overall_rating = graded_assessment.overall_rating
    print(assessment_grade_level)
    

    student_instance.overall_rating = f'Grade {assessment_grade_level} - {assessment_overall_rating}'
    student_instance.save()
