from django import forms 
from arch_portal.domain.models.famille import Famille
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        exclude = ["galerie"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-8'),
                Column('famille_mere', css_class='col-md-4'),
                Column('description', css_class='col-md-6'),
                Column('origine', css_class='col-md-6'),
                Column('histoire', css_class='col-md-12'), 
                css_class='row'
            ),
            Row(
                Column('communaute', css_class='col-md-4'),
                Column('chef', css_class='col-md-4'),
                Column('type', css_class='col-md-4'),
                css_class='row'
            ),
        )