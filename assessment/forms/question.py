from django import forms


class AssessmentQuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(AssessmentQuestionForm, self).__init__(*args, **kwargs)

        self.fields['question_content'] = forms.CharField(
            label = '',
            initial = question.question_content,
            widget=forms.Textarea(attrs={
                'class': 'form-control my-2 border-secondary bg-secondary text-light',
                'readonly': 'readonly',
                'rows': 2,
                'style': 'resize:none; font-size: 32px; '
            }),
        )
        QUESTION_CHOICES = [(choice.id, choice.choice_content) for choice in question.get_choices()]

        answer_field_name = f'answer_content_{question.id}'
        self.fields[answer_field_name] = forms.ChoiceField(
            label = '', 
            choices=QUESTION_CHOICES,
            widget=forms.RadioSelect,
            required=True,
        )

