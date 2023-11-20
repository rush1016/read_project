from django import forms

from materials.models import Passage

class PassageAdminForm(forms.ModelForm):
    # Define a custom form with a CharField using a Textarea widget
    passage_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Passage
        fields = '__all__'