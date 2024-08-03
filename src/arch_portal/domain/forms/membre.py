
from django import forms
from arch_portal.use_cases.services.core import compute_sha1
from crispy_forms.helper import FormHelper
from arch_portal.domain.models.membre import Membre 
class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries"]
 
class UsersLoginForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['login','pwd']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

class UsersSubscribeForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ["nomcomplet","login","pwd","email","telephone","sexe","datenaissance","lieunaissance","residence"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.pwd = compute_sha1(self.cleaned_data['pwd']) 
        if commit:
            user.save()
        return user
        