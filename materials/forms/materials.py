from django import forms
from materials.models import Passage, Question, Choice
from django.forms import inlineformset_factory, BaseInlineFormSet


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
            'rows': 2,
            'required': 'required',
            }
        ),
    )


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_content', 'is_correct']

    choice_content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-2',
            'placeholder': 'Add choice here',
            'required': 'required',
            }
        )
    )
    is_correct = forms.BooleanField(
        label='Correct Answer',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input m-0'
            }
        ),
        required=False
    )


class BaseQuestionFormset(BaseInlineFormSet):
    class Meta:
        model = Question
        fields = ['question_content', ]

    def add_fields(self, form, index):
        super(BaseInlineFormSet, self).add_fields(form, index)

        form.nested = ChoiceFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='address-%s-%s' % (
                form.prefix,
                ChoiceFormset.get_default_prefix()),
        )
    
    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result
    
    def save(self):
        result = super(BaseQuestionFormset, self).save()

        for form in self.forms:
            if hasattr(form, 'nested'):
             if not self._should_delete_form(form):
                    form.nested.save()

        return result


QuestionFormset = inlineformset_factory(
    Passage,
    Question,
    form=QuestionForm,
    formset=BaseQuestionFormset,
    fields=['question_content'],
    can_delete=False,
    extra=0,
    min_num=1,
)


ChoiceFormset = inlineformset_factory(
    Question,
    Choice,
    form=ChoiceForm,
    fields=['choice_content', 'is_correct'],
    can_delete=False,
    extra=0,
    min_num=4,
)