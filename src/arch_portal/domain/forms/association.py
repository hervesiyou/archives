from arch_portal.domain.models.association import Association
from django.forms import ModelForm

class AssociationForm(ModelForm):
    class Meta:
        model = Association
        exclude  = [""]

    
