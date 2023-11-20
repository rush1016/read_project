def calculate_recommended_grade_level(assessment_instance):
    student_instance = assessment_instance.student
    assessment_grade_level = assessment_instance.grade_level
    graded_assessment = assessment_instance.graded_assessment
    overall_rating = graded_assessment.overall_rating

    print(overall_rating)

    if assessment_grade_level >= 2:
        if overall_rating == "Frustration":
            recommended_grade = assessment_grade_level-1
    
        elif overall_rating == "Independent":
            recommended_grade = assessment_grade_level+1

        else:
            recommended_grade = assessment_grade_level+1

    student_instance.recommended_grade_level = recommended_grade
    student_instance.save()

