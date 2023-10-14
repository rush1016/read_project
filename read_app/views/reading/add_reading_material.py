from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from read_app.forms.materials import (
    PassageForm, 
    QuestionFormset
)


@transaction.atomic # To group series of database transactions into one
def add_reading_material(request):
    if request.method == 'POST':
        # Save the passage
        passage_form = PassageForm(request.POST)
        passage_instance = passage_form.save()
        print(type(passage_instance))

        # Save the questions and choices
        # Using the saved passage_instance as the foreign key
        question_formset = QuestionFormset(request.POST, instance=passage_instance)
        if question_formset.is_valid():
            question_formset.save()

            messages.success(request, 'Successfully added reading material!')
            return redirect('reading_material')

        else:
            messages.error(request, question_formset.errors)
            messages.error(request, 'Unable to add reading material.')
            return redirect('reading_material')
        
    else:
        passage_form = PassageForm()
        question_formset = QuestionFormset()

    context = {
        'passage_form': passage_form,
        'question_formset': question_formset,
    }

    return render(request, 'reading/add_reading_material.html', context)