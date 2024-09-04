from arch_portal.domain.models.association import Association
from django.forms import ModelForm,ValidationError
from crispy_forms.helper import FormHelper

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

    
