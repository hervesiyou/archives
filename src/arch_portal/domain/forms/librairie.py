from arch_portal.domain.models.librairie import Librairie
from django.forms import ModelForm,ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

class LibrairieForm(ModelForm):
    class Meta:
        model = Librairie
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        type = cleaned_data.get("type")
        possesseur = cleaned_data.get("possesseur")
        if Librairie.objects.filter(nom=nom, type=type, possesseur=possesseur).exists() :
            raise ValidationError("Cette librairie existe dejà en base")
        return cleaned_data
        
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
