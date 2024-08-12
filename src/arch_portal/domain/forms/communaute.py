
from django import forms
from arch_portal.domain.models.communaute import Communaute 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
class CommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude  = ["chef"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-12'),
                Column('description', css_class='col-md-12'),
            ),
            Row(
                Column('histoire', css_class='col-md-6'),
                Column('geographie', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column('origine', css_class='col-md-3'),
                Column('region', css_class='col-md-3'),
                Column('superficie', css_class='col-md-3'),
                Column('type', css_class='col-md-3'),
                css_class='row'
            ),
        )
