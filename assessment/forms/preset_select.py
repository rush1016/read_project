from django import forms
from materials.models import AssessmentPreset


class PresetSelect(forms.Form):
    PRESET_CHOICES = [(preset.id, preset.name) for preset in AssessmentPreset.objects.all()]


    preset_select = forms.ChoiceField(
        label='',
        choices = PRESET_CHOICES,
        widget= forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
    )