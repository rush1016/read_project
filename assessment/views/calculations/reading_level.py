from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction


from utils.graded_assessment_calculations import GradedAssessmentCalculations
from assessment.models import AssessmentSession


@transaction.atomic
def calculate_reading_level_view(request, assessment_id):
    assessment = AssessmentSession.objects.get(pk=assessment_id)

    if assessment.is_finished:
        # Calculate reading score and ratings
        GradedAssessmentCalculations.calculate_oral_reading(assessment)
        GradedAssessmentCalculations.calculate_reading_comprehension(assessment)
        GradedAssessmentCalculations.calculate_passage_overall_rating(assessment)
        GradedAssessmentCalculations.calculate_recommended_grade_level(assessment)
        GradedAssessmentCalculations.calculate_rating_per_grade_level(assessment)
        GradedAssessmentCalculations.calculate_student_overall_rating(assessment)

        messages.success(request, 'Successfully calculated scores and ratings.')

    else:
        messages.error(request, 'Assessment session not yet finished. Please wait for your student to submit their assessment form.')
    
    return redirect('assessment_session', assessment_id=assessment_id)
    

