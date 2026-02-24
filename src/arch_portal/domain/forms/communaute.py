
from django import forms
from arch_portal.domain.models.communaute import Communaute 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class CommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude  = ["chef"]

    def clean(self):

        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        type = cleaned_data.get("type")
        origine = cleaned_data.get("origine")
        region = cleaned_data.get("region")

        if Communaute.objects.filter(nom=nom, type=type, origine=origine,region=region).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Cette communauté existe dejà !")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-10'),
                Column('publique', css_class='col-md-2 div-check'),
                Column('description', css_class='col-md-12'),
            ),
            Row(
                Column('histoire', css_class='col-md-6'),
                Column('histoires', css_class='col-md-3'),
                Column('geographie', css_class='col-md-3'),
                css_class='row'
            ),
            Row(
                Column('origine', css_class='col-md-3'),
                Column('region', css_class='col-md-3'),
                Column('superficie', css_class='col-md-3'),
                Column('type', css_class='col-md-3'),
                css_class='row'
            ),
            Row(
                Column('legende_fondatrice', css_class='col-md-6'),
                Column('histoire_detaillee', css_class='col-md-6'),
                # Column('superficie', css_class='col-md-3'),
                # Column('type', css_class='col-md-3'),
                css_class='row'
            ),
        )
