from arch_portal.domain.models.evenement import Evenement
from django.forms import ModelForm
from crispy_forms.helper import FormHelper


class EvenementForm(ModelForm):
    class Meta:
        model = Evenement
        exclude = [""]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False