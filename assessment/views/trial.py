from django.shortcuts import render

from materials.models import Passage
from assessment.models import AssessmentMiscue

def test(request):
    passage = Passage.objects.get(pk=2)

    words = passage.passage_content.split()
    miscues = AssessmentMiscue.objects.filter(passage=passage)
    miscue_words = {miscue.word: miscue.miscue for miscue in miscues}

    context = {
        'words': words,
        'passage': passage,
        'miscue_words': miscue_words,
    }

    return render(request, 'assessment/try.html', context)