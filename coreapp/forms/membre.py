
from django import forms

from coreapp.models.membre import Membre 
class MembreForm(forms.ModelForm):
    
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries"]
 