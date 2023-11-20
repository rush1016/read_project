from django import forms

class GstScoreForm(forms.Form):
    LANGUAGES = (
        ('English', 'English'),
        ('Filipino', 'Filipino'),
    )
    gst_score = forms.CharField(
        label = 'GST Score',
        widget= forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Group Screening Test Score here',
            }
        ),
        help_text= '<ul class="text-muted"><li>Enter a value between 0-20</li></ul>'
    )
    language = forms.ChoiceField(
        choices=LANGUAGES,
        widget= forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )

    def clean_gst_score(self):
        gst_score = self.cleaned_data.get('gst_score')

        try:
            gst_score = float(gst_score)
        except (TypeError, ValueError):
            raise forms.ValidationError('Invalid GST Score. Please enter a numeric value.')

        if not 0 <= gst_score <= 20:
            raise forms.ValidationError('GST Score must be between 0 and 20.')

        return gst_score