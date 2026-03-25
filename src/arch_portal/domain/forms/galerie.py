
from django import forms
from arch_portal.domain.models.galerie import Galerie
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class GalerieForm(forms.ModelForm):
    class Meta:
        model = Galerie
        exclude  = ["images"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nom"].widget.attrs.update({"class":" form-control","title":"Nom de la galerie"}   )
        self.fields["description"].widget.attrs.update({"class":" form-control","title":"Description de la galerie"}   )

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-12'),
                Column('description', css_class='col-md-12'),
                # Column('geographie', css_class='col-md-3'),
                css_class='row'
            ),
            Row(
                Column('communaute', css_class='col-md-3'),
                Column('association', css_class='col-md-3'),
                Column('famille', css_class='col-md-3'),
                Column('evenement', css_class='col-md-3'),
            ),
            
        )
        
