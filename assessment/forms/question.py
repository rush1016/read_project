from django import forms


class AssessmentQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        selected_choice_id = kwargs.pop('selected_choice_id', None) # Previously submitted answers
        
        super(AssessmentQuestionForm, self).__init__(*args, **kwargs)

        QUESTION_CHOICES = [(choice.id, choice.choice_content) for choice in question.get_choices()]
        print(selected_choice_id)


        answer_field_name = f'answer_content_{question.id}'
        self.fields[answer_field_name] = forms.ChoiceField(
            label = '', 
            choices=QUESTION_CHOICES,
            widget=forms.RadioSelect(
                attrs={
                    'class': 'radio-div',
                }
            ),
            required=True,
            initial=selected_choice_id, # Set the previously submitted answers as initial
        )

