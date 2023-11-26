from django.http import JsonResponse

from assessment.models import AssessmentSession, AssessmentSessionPassage
from students.models import Student

def check_existing_screening(request):
    if request.method == 'GET':
        student_id = request.GET.get('studentId')
        student = Student.objects.get(pk=student_id)
        language = request.GET.get('language')
        assessment_type = 'Screening'

        # Get the Screening Test Instances
        assessment_session = AssessmentSession.objects.filter(
            student = student,
            assessment_type = assessment_type, 
        ).first()
        screening_exists = AssessmentSessionPassage.objects.filter(
            assessment=assessment_session,
            langauge=language,
        ).exists()

        return JsonResponse({"success": True, "exists": screening_exists})

