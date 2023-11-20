from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from materials.models import Passage

@login_required
def to_reading_materials(request):
    passages = Passage.objects.all().order_by('set')
    context = {
        'passages': passages
    }
    return render(request, 'reading/reading_materials.html', context)