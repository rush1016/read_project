from students.models import StudentRating
from assessment.models import AssessmentSession

class ScreeningTestCalculations():
    @staticmethod
    def calculate_screening_rating(assessment_instance):
        student_instance = assessment_instance.student
        language = assessment_instance.get_passages()[0].passage.language
        gst_score = assessment_instance.total_score

        # Check if it's a Screening Assessment and the student has passed the screening test
        if assessment_instance.assessment_type == 'Screening':
            if gst_score >= 14:
                overall_rating = f'Passed Screening Test ({language})'
            else:
                overall_rating = 'Further Assessment Required'

            # Update the student's overall_rating
            student_instance.overall_rating = overall_rating
            student_instance.is_screened= True
            student_instance.save()


            recommended_grade = calculate_screening_recommended_grade(student_instance, gst_score)

            set_recommended_grade(student_instance, language, recommended_grade)


    @staticmethod
    def calculate_screening_rating_add(student, gst_score, language):
        student_rating = student.student_rating
        if gst_score:
            student.gst_score = gst_score
            set_gst_score(student_rating, language, gst_score)

            recommended_grade = calculate_screening_recommended_grade(student, gst_score)

            set_recommended_grade(student_rating, language, recommended_grade)

            if 0 < gst_score < 15:
                rating = 'Further assessments required'
                
            elif gst_score >= 15:
                rating = f'Grade {student.grade_level} - Independent'

        else:
            rating = 'Not yet screened'


        set_rating_field(language, student_rating, rating)
        student.overall_rating = rating
        student.is_screened = True
        student_rating.save()
        student.save() 


    @staticmethod
    def calculate_screening_scores(student, assessment):
        gst_score = assessment.total_score
        language = assessment.get_passages()[0].passage.language
        student_rating = student.student_rating

        # If assessment is finished
        # Save the scores
        if gst_score:
            recommended_grade_level = calculate_screening_recommended_grade(student, gst_score)

            student.recommended_grade_level = recommended_grade_level

            # Functions check the language of the material before saving
            set_gst_score(student_rating, language, gst_score)

            set_recommended_grade(student_rating, language, recommended_grade_level)

        student.save()


def set_gst_score(student_rating, language, gst_score):
    if language == 'English':
        student_rating.english_gst_score = gst_score
    elif language == 'Filipino':
        student_rating.filipino_gst_score = gst_score


def set_recommended_grade(student_rating, language, recommended_grade_level):
    if language == 'English':
        # English materials are only recommended for Second Grade and above
        if recommended_grade_level == 1:
            recommended_grade_level += 1
        student_rating.english_recommended_grade = recommended_grade_level
    elif language == 'Filipino':
        student_rating.filipino_recommended_grade = recommended_grade_level

    student_rating.save()


def calculate_screening_recommended_grade(student, gst_score):
    if 8 <= gst_score <= 13:
        recommended_grade_level = student.grade_level-2
    elif 0 <= gst_score <= 7:
        recommended_grade_level = student.grade_level-3
    else:
        recommended_grade_level = student.grade_level

    return recommended_grade_level


def set_rating_field(language, student_rating, rating):
    if language == 'English':
        student_rating.english_rating = rating

    elif language == 'Filipino':
        student_rating.filipino_rating = rating