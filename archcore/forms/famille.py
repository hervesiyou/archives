from django import forms 
from coreapp.models.famille import Famille
class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        exclude = ["galerie"]