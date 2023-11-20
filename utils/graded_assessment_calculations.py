from students.models import StudentRating

class GradedAssessmentCalculations():
    @staticmethod
    def calculate_oral_reading(assessment_instance):
        assessment = assessment_instance
        passage = assessment.get_passages()[0].passage # Get the first and only passage
        graded_assessment = assessment_instance.graded_assessment

        miscues_count = assessment.get_miscues().count()
        word_count = passage.passage_length

        # Formula
        oral_reading_score = ((word_count-miscues_count)/word_count)*100

        if 97 <= oral_reading_score <= 100:
            rating = 'Independent'
        elif 90 <= oral_reading_score <= 96:
            rating = 'Instructional'
        else:
            rating = 'Frustration'

        graded_assessment.oral_reading_score = oral_reading_score
        graded_assessment.oral_reading_rating = rating
        graded_assessment.save()


    @staticmethod
    def calculate_reading_comprehension(assessment_instance):
        assessment = assessment_instance
        graded_assessment = assessment_instance.graded_assessment
        total_score = assessment.total_score
        question_count = assessment.number_of_questions

        # Formula
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
    

    @staticmethod
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


    @staticmethod
    def calculate_student_overall_rating(assessment_instance):
        graded_assessment = assessment_instance.graded_assessment
        passage = assessment_instance.get_passages()[0].passage
        passage_language = passage.language
        student_instance = assessment_instance.student

        assessment_grade_level = passage.grade_level
        assessment_overall_rating = graded_assessment.overall_rating

        student_instance.overall_rating = f'Grade {assessment_grade_level} - {assessment_overall_rating}'
        student_instance.save()


    @staticmethod
    def calculate_rating_per_grade_level(assessment_instance):
        assessment_grade_level = assessment_instance.grade_level
        assessment_language = assessment_instance.get_graded_passage().passage.language
        overall_rating = assessment_instance.graded_assessment.overall_rating
        student = assessment_instance.student

        english_rating = f'Grade {assessment_grade_level} - {overall_rating}' if assessment_language == 'English' else None
        filipino_rating = f'Grade {assessment_grade_level} - {overall_rating}' if assessment_language == 'Filipino' else None

        recommended_grade = assessment_grade_level+determine_grade_offset(overall_rating)
        if recommended_grade == 0:
            recommended_grade = 1

        student_rating = StudentRating.objects.get_or_create(
            student = student,
        )[0]

        if not english_rating == None:
            student_rating.english_rating = english_rating
            student_rating.english_recommended_grade = recommended_grade
        if not filipino_rating == None:
            student_rating.filipino_rating = filipino_rating
            student_rating.filipino_recommended_grade = recommended_grade

        student_rating.save()


        if assessment_grade_level == 1:
            if assessment_language == 'English':
                student_rating.first_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.first_grade_fil = overall_rating
        elif assessment_grade_level == 2:
            if assessment_language == 'English':
                student_rating.second_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.second_grade_fil = overall_rating
        elif assessment_grade_level == 3:
            if assessment_language == 'English':
                student_rating.third_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.third_grade_fil = overall_rating
        elif assessment_grade_level == 4:
            if assessment_language == 'English':
                student_rating.fourth_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.fourth_grade_fil = overall_rating
        elif assessment_grade_level == 5:
            if assessment_language == 'English':
                student_rating.fifth_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.fifth_grade_fil = overall_rating
        elif assessment_grade_level == 6:
            if assessment_language == 'English':
                student_rating.sixth_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.sixth_grade_fil = overall_rating
        elif assessment_grade_level == 7:
            if assessment_language == 'English':
                student_rating.seventh_grade_eng = overall_rating
            elif assessment_language == 'Filipino':
                student_rating.seventh_grade_fil = overall_rating

        student.save()
        student_rating.save()


    @staticmethod
    def calculate_recommended_grade_level(assessment_instance):
        student_instance = assessment_instance.student
        assessment_grade_level = assessment_instance.grade_level
        graded_assessment = assessment_instance.graded_assessment
        overall_rating = graded_assessment.overall_rating

        recommended_grade = assessment_grade_level+determine_grade_offset(overall_rating)

        student_instance.recommended_grade_level = recommended_grade
        student_instance.save()


def determine_grade_offset(overall_rating):
        if overall_rating == "Frustration":
            return -1
        elif overall_rating == "Independent":
            return 1
        else:
            return 1