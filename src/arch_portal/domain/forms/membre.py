
from django import forms
from arch_portal.use_cases.services.core import compute_sha1
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from arch_portal.domain.models.membre import Membre 

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        exclude = ["etatvalidation","dateinscription","approbateurs","galeries"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            Row(
                Column('nomcomplet', css_class='col-md-12'),
                Column('login', css_class='col-md-6'),
                Column('pwd', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
                Column('telephone', css_class='col-md-6'),
                Column('type', css_class='col-md-2'), 
                Column('sexe', css_class='col-md-2'), 
                Column('etatcivil', css_class='col-md-2'), 
                Column('nbenfant', css_class='col-md-2'), 
                Column('vivant', css_class='col-md-2'), 
                Column('datedeces', css_class='col-md-2'), 
                Column('datenaissance', css_class='col-md-3'), 
                Column('lieunaissance', css_class='col-md-3'), 
                Column('residence', css_class='col-md-3'), 
                Column('notabilite', css_class='col-md-3'), 
                css_class='row'
            ),
            Row(
                Column('education', css_class='col-md-3'), 
                Column('diplomes', css_class='col-md-3'), 
                Column('profession', css_class='col-md-3'), 
                Column('associations', css_class='col-md-3'), 
                Column('familles', css_class='col-md-12'), 
                Column('pere', css_class='col-md-6'), 
                Column('mere', css_class='col-md-6'), 
                
                css_class='row'
            ),
        )
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

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nomcomplet")
        sexe = cleaned_data.get("type")
        pere = cleaned_data.get("pere")
        if Membre.objects.filter(nom=nom, sexe=sexe, pere=pere).exists():
            raise forms.ValidationError("Ce membre existe dejà ! ")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.pwd = compute_sha1(self.cleaned_data['pwd']) 
        if commit:
            user.save()
        return user
        