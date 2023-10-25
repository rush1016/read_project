from django.shortcuts import render, get_list_or_404

from assessment.models import AssessmentSession

def assessment_list_view(request):
    assessments = AssessmentSession.objects.all()

    context = {
        'assessments': assessments,
    }

    return render(request, 'assessment/assessment_list.html', context)
