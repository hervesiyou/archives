from arch_portal.domain.models.librairie import Librairie
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
class LibrairieForm(ModelForm):
    class Meta:
        model = Librairie
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nom', css_class='col-md-6'),
                Column('possesseur', css_class='col-md-6'),
                Column('description', css_class='col-md-12'),
                css_class='row'
            ),
            Row(
                Column('type', css_class='col-md-6'),
                Column('lieu', css_class='col-md-6'),
                css_class='row'
            ),
        )