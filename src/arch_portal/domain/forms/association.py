from arch_portal.domain.models.association import Association
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

class AssociationForm(ModelForm):
    class Meta:
        model = Association
        exclude  = [""]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    
