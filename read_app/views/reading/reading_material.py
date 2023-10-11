from django.shortcuts import render, redirect, get_object_or_404

from read_app.models import Passage
from read_app.forms.materials import PassageForm, QuestionFormSet, ChoiceFormSet

def to_reading_materials(request):
    return render(request, 'reading/reading_materials.html')


def generate_unique_id():
    count = Passage.objects.count() + 1
    if Passage.objects.filter(id=count).exists():
        count += 1
    return count


def to_add_reading_material(request):
    passage_id = generate_unique_id()
    passage_form = PassageForm()
    question_formset = QuestionFormSet()
    choice_formset = ChoiceFormSet()

    context = {
        'passage_id': passage_id,
        'passage_form': passage_form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    }

    return render(request, 'reading/add_reading_material.html', context)