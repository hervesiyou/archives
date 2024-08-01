from arch_portal.domain.models.livre import Livre
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class LivreForm(ModelForm):
    class Meta:
        model = Livre
        exclude = ["librairies"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-6'),
                Column('auteur', css_class='col-md-6'),
                Column('description', css_class='col-md-12'),
                css_class='row'
            ),
            Row(
                Column('domaine', css_class='col-md-6'),
                Column('prix', css_class='col-md-6'),
                css_class='row'
            ),
        )