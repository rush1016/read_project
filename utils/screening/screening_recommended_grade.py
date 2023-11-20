def calculate_screening_recommended_grade(student):
    if 8 <= student.gst_score <= 13:
        student.recommended_grade_level = student.grade_level-2
    elif 0 <= student.gst_score <= 7:
        student.recommended_grade_level = student.grade_level-3

    student.save()