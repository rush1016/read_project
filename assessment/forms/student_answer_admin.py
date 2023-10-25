from django import forms

from assessment.models import StudentAnswer

class StudentAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = StudentAnswer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentAnswerAdminForm, self).__init__(*args, **kwargs)
        if self.instance.passage:
            self.fields['question'].queryset = self.instance.passage.get_questions()

        if self.instance.question:
            # Filter the answer_content choices based on the related question
            self.fields['answer'].queryset = self.instance.question.get_choices()

