def calculate_screening_rating(student):
    if student.gst_score == 0:
        student.overall_rating = 'Not yet screened'
    elif 0 < student.gst_score < 14:
        student.overall_rating = 'Further Assessment Required'
        student.is_screened = True
                
    elif student.gst_score >= 14:
        student.overall_rating = 'Passed Screening Test'
        student.is_screened = True

    student.save() 