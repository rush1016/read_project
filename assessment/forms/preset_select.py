from django import forms
from materials.models import AssessmentPreset


class PresetSelect(forms.Form):

    preset_select = forms.ChoiceField(
        label='',
        choices = [],
    )

    def __init__(self, *args, **kwargs):
        grade_level = kwargs.pop('grade_level', None)
        super(PresetSelect, self).__init__(*args, **kwargs)

        if grade_level:
            PRESET_CHOICES = [(preset.id, preset.name) for preset in AssessmentPreset.objects.filter(grade_level=grade_level)]
        else:
            PRESET_CHOICES = [(preset.id, preset.name) for preset in AssessmentPreset.objects.all()]

        self.fields['preset_select'] = forms.ChoiceField(
            label='',
            choices=PRESET_CHOICES,
            widget= forms.Select(
                attrs={
                'class': 'form-select',
                }
            ),
        )