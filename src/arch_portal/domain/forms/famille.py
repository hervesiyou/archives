from django import forms 
from arch_portal.domain.models.famille import Famille
class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        exclude = ["galerie"]