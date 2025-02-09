from arch_portal.domain.models.association import Association
from django.forms import ModelForm,ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class AssociationForm(ModelForm):
    class Meta:
        model = Association
        exclude  = [""]

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        communaute = cleaned_data.get("communaute")
        localisation = cleaned_data.get("localisation")
        if Association.objects.filter(nom=nom, communaute=communaute, localisation=localisation).exists():
            raise ValidationError("Cette association existe dejà !")
        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-8'),
                Column('publique', css_class='col-md-4 div-check'),
                Column('description', css_class='col-md-3'),
                Column('adhesion', css_class='col-md-3'),
                Column('localisation', css_class='col-md-3'),
                Column('contact', css_class='col-md-3'), 
                css_class='row'
            ),
            Row(
                Column('communaute', css_class='col-md-4'),
                Column('famille', css_class='col-md-4'),
                Column('type', css_class='col-md-4'),
                css_class='row'
            ),
        )

    
