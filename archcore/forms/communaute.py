
from django import forms

from coreapp.models.communaute import Communaute 

class CommunauteForm(forms.ModelForm):
    
    class Meta:
        model = Communaute
        exclude  = ["chef"]
