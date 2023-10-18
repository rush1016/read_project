from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from read_app.models import Passage

@login_required
def to_reading_materials(request):
    passages = Passage.objects.all().order_by('id')
    context = {
        'passages': passages
    }
    return render(request, 'reading/reading_materials.html', context)