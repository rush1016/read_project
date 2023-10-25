from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from materials.forms.materials import PassageForm, QuestionFormset
from materials.models import Passage

@login_required
@transaction.atomic
def manage_passage(request, passage_id):
    passage = get_object_or_404(Passage, pk=passage_id)

    if request.method == 'POST':
        passage_form = PassageForm(request.POST, instance=passage)
        question_formset = QuestionFormset(request.POST, instance=passage)
        if not passage_form.is_valid():
            messages.error(request, passage_form.errors)
            return redirect('manage_passage', passage_id=passage_id)

        if not question_formset.is_valid():
            messages.error(request, 'Questions are not valid.')
            return redirect('manage_passage', passage_id=passage_id)
        
        passage_form.save()
        question_formset.save()
        messages.success(request, 'Reading material saved.')
        return redirect('manage_passage', passage_id=passage_id)


    else:
        passage_form = PassageForm(instance=passage)
        question_formset = QuestionFormset(instance=passage)


    context = {
        'passage': passage,
        'passage_form': passage_form,
        'question_formset': question_formset,
    }
    return render(request, 'reading/manage_passage.html', context)