from django.shortcuts import render, get_object_or_404

from read_app.models import Passage

def to_reading_materials(request):
    passages = Passage.objects.all()
    context = {
        'passages': passages
    }
    return render(request, 'reading/reading_materials.html', context)