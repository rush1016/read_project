from django import forms
from read_app.models import Passage, Question, Choice
from django.forms import inlineformset_factory


class PassageForm(forms.ModelForm):
    class Meta:
        model = Passage
        fields = ['grade_level', 'passage_title', 'passage_content']

    passage_title = forms.CharField(
        label='Passage Title',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    passage_content = forms.CharField(
        label='Passage Content',
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    grade_level_choices = [
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
    ]
    grade_level = forms.ChoiceField(
        label='Grade Level',
        choices=grade_level_choices,
        widget=forms.Select(attrs={'class': 'form-select'}))


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_content']
    question_content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control mt-5', 
            'placeholder': 'Add a question here', 
            'rows': 2
            }
        ),
    )

QuestionFormSet = inlineformset_factory(Passage, Question, QuestionForm, extra=1, can_delete=False)


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_content', 'is_correct']

    choice_content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Add choice here',
            }
        )
    )
    is_correct = forms.BooleanField(
        label='Correct Answer',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
            }
        ),
        required=False
    )

ChoiceFormSet = inlineformset_factory(Question, Choice, ChoiceForm, extra=4, can_delete=False)