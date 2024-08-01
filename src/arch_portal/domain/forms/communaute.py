
from django import forms
from arch_portal.domain.models.communaute import Communaute 

class CommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude  = ["chef"]
