from django import forms 
from arch_portal.domain.models.famille import Famille
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        exclude = ["galerie"]

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        type = cleaned_data.get("type")
        famille_mere = cleaned_data.get("famille_mere")
        if Famille.objects.filter(nom=nom, type=type, famille_mere=famille_mere).exists():
            raise forms.ValidationError("Cette Famille existe dejà ! ")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-6'),
                Column('famille_mere', css_class='col-md-3'),
                Column('publique', css_class='col-md-3 div-check'),
                Column('description', css_class='col-md-6'),
                Column('origine', css_class='col-md-6'),
                Column('histoire', css_class='col-md-12'), 
                css_class='row'
            ),
            Row(
                Column('communaute', css_class='col-md-4'),
                Column('chef', css_class='col-md-4'),
                Column('type', css_class='col-md-4'),
                # Column('image', css_class='col-md-6'),
                Column('urlgoogle', css_class='col-md-12'),
                css_class='row'
            ),
        )