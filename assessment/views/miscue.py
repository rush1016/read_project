from django.http import JsonResponse, Http404
from django.db import transaction

from assessment.models import AssessmentSession, AssessmentMiscue
from materials.models import Passage

def save_miscue_view(request):
    passage_id = request.POST.get('passage_id')
    assessment_id = request.POST.get('assessment_id')
    word = request.POST.get('word')
    miscue = request.POST.get('miscue').strip()
    index = request.POST.get('index').strip()

    passage = Passage.objects.get(pk=passage_id)
    assessment = AssessmentSession.objects.get(pk=assessment_id)
    AssessmentMiscue.objects.update_or_create(
        assessment=assessment,
        passage=passage,
        word=word,
        miscue=miscue,
        index=index,
    )

    return JsonResponse({"success": True})


@transaction.atomic
def get_miscue_view(request):
    assessment_id = request.GET.get('assessment_id')

    try:
        assessment = AssessmentSession.objects.get(pk=assessment_id)
        assessment_passage = assessment.get_passages()[0]
        passage = assessment_passage.passage
        words = passage.passage_content.split()
        miscues = AssessmentMiscue.objects.filter(assessment=assessment)

        miscues_list = [
            {"word": miscue.word, 'miscue': miscue.miscue, 'index': miscue.index} for miscue in miscues
        ]
        return JsonResponse({"success": True, "words": words, "miscues": miscues_list})

    except Http404:
        return JsonResponse({"success": False, "error": "404"})


@transaction.atomic
def delete_miscue_view(request):
    passage_id = request.POST.get('passage_id')
    assessment_id = request.POST.get('assessment_id')

    passage = Passage.objects.get(pk=passage_id)
    assessment = AssessmentSession.objects.get(pk=assessment_id)
    
    word = request.POST.get('word') 
    index = request.POST.get('index') 

    miscue = AssessmentMiscue.objects.get(assessment=assessment, passage=passage, word=word, index=index)
    miscue.delete()

    return JsonResponse({"success": True})
