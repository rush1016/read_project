from django.shortcuts import redirect, render
from django.contrib import messages

from materials.forms.materials import QuestionForm, ChoiceForm
from materials.models import Passage, Choice

def create_question(request, passage_id):
    if request.method == 'POST':
        passage = Passage.objects.get(pk=passage_id)
        question_form = QuestionForm(request.POST)

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.passage = passage
            
            raw_question_content = question_form.cleaned_data.get('question_content', '')
            cleaned_question_content = raw_question_content.split('.', 1)[-1].strip()
            question.question_content = cleaned_question_content

            # Extract choices from the form and associate them with the question
            raw_choices = request.POST.get('choice_content', '')
            choices_data = [choice.strip() for choice in raw_choices.split('\n') if choice.strip()]

            # Save the question and choices
            question.save()

            choices = []
            for choice_data in choices_data:
                is_correct = choice_data.startswith('*')
                choice_content = choice_data.lstrip('*').split('.', 1)[-1].strip()
                choice = Choice(question=question, choice_content=choice_content, is_correct=is_correct)
                choices.append(choice)

            Choice.objects.bulk_create(choices)
            messages.success(request, 'Success')
        else:
            messages.error(request, question_form.errors)
        
        return redirect('create_question', passage_id)

    else:
        context = {
            'question_form': QuestionForm(),
            'choice_form': ChoiceForm(),
            'passage': Passage.objects.get(pk=passage_id),
        }
        
    return render(request, 'reading/create_question.html', context)