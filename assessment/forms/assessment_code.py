from django import forms

class AssessmentCodeForm(forms.Form):
    passcode = forms.CharField(
        label = 'Assessment passcode',
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter 6-character passcode here',
            }
        ),
        help_text='<ul><li>Ask your teacher for your assessment code.</li><li>Read each instructions carefully before answering.</li><li>Answer all the questions in the assessment.</li><li>Choose the correct answer from the given choices.</li></ul>'

    )