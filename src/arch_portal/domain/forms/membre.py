
from django import forms
from arch_portal.domain.models.membre import Membre 
class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries"]
 
class UsersLoginForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['login','pwd']