from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db import transaction

from read_app.forms.materials import PassageForm
from read_app.models import Passage

def add_passage(request):
    passage_form = PassageForm(request.POST or None)

    if passage_form.is_valid():
        passage_instance = passage_form.save(commit=False)
        # Use generated passage_id from the hidden field in the form
        passage_instance.id = request.POST['passage_id']
        passage_instance.save()

        messages.success(request, 'Successfully added reading material!')
        return JsonResponse({"success": True})

    else:
        messages.error(request, passage_form.errors)
        return JsonResponse({"success": False})
    

@transaction.atomic # To group series of database transactions into one
def add_question(request):
    if request.method == 'POST':
        # Get passage id from the hidden field
        passage_id = request.POST['passage_id']
        # Create instance of Passage model and use as foreign key
        # for each question
        passage_instance = get_object_or_404(Passage, pk=passage_id)
        question_formset = QuestionFormSet(request.POST, instance=passage_instance)
        if question_formset.is_valid():
            questions = question_formset.save()

            for question in questions:
                # Use each question form as foreign key for each choice
                choice_formset = ChoiceFormSet(request.POST, instance=question)
                choices = choice_formset.save()
                # Add each choice
                for choice in choices:
                    choice.save()
            messages.success(request, 'Successfully added reading material!')
            return JsonResponse({"success": True})

        else:
            messages.error(request, 'Error: ', question_formset.errors)
            return JsonResponse({"success": False})

    # If request method is not POST send back the forms and passage_id
    # to generate more question forms to be submitted
    passage_id = request.GET.get('passage_id')
    question_formset = QuestionFormSet()
    choice_formset = ChoiceFormSet()
    context = {
        'question_formset': question_formset,
        'choice_formset': choice_formset,
        'passage_id': passage_id
    }

    return render(request, 'reading/partial_question_form.html', context)