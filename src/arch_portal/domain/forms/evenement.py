from arch_portal.domain.models.evenement import Evenement
from django.forms import ModelForm,ValidationError
from crispy_forms.helper import FormHelper


class EvenementForm(ModelForm):
    class Meta:
        model = Evenement
        exclude = [""]

    def clean(self):
        cleaned_data = super().clean()
        titre = cleaned_data.get("titre")
        communaute = cleaned_data.get("communaute")
        description = cleaned_data.get("description")
        if Evenement.objects.filter(titre=titre, communaute=communaute, description=description).exists():
            raise ValidationError("Cet evenement existe dejà ! ")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False