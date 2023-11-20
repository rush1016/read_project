def calculate_passage_overall_rating(assessment_instance):
    graded_assessment = assessment_instance.graded_assessment
    oral_rating = graded_assessment.oral_reading_rating
    comprehension_rating = graded_assessment.reading_comprehension_rating

    if oral_rating == "Frustration":
        overall_rating = "Frustration"

    elif oral_rating == "Instructional":
        if comprehension_rating == "Independent" or comprehension_rating == "Instructional":
            overall_rating = "Instructional"
        elif comprehension_rating == "Frustration":
            overall_rating = "Frustration"

    elif oral_rating == "Independent":
        if comprehension_rating == "Independent":
            overall_rating = "Independent"
        elif comprehension_rating == "Instructional":
            overall_rating = "Instructional"
        else:
            overall_rating = "Frustration"


    # Calculate Overall Rating based on Oral Reading Rating and Comprehension Rating
    graded_assessment.overall_rating = overall_rating
    graded_assessment.save()