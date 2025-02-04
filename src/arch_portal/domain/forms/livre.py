from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.image import Image
from django.forms import ModelForm,ValidationError, modelformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column,Fieldset, HTML
  

class ImageInlineForm(ModelForm):
    class Meta:
        model = Image
        fields = ('fichier',)

ImageFormSet = modelformset_factory(Image, form=ImageInlineForm, extra=3)

class LivreForm(ModelForm):
    # images = forms.ModelMultipleChoiceField(queryset=Image.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Livre
        exclude = ["librairies"]

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get("nom")
        auteur = cleaned_data.get("auteur")
        prix = cleaned_data.get("prix")
        if Livre.objects.filter(nom=nom, auteur=auteur, prix=prix).exists():
            raise ValidationError("Ce livre existe dejà !")
        return cleaned_data

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
                Column('type', css_class='col-md-2 typeClass'),
                Column('file', css_class='col-md-2 fichierClass'),
                Column('stock', css_class='col-md-1 stockClass'),
                Column('domaine', css_class='col-md-4'),
                Column('prix', css_class='col-md-4'),
                css_class='row'
            ), 
            Fieldset(
                '',
                HTML('<div id="form-container"> <div id="id_images_0"></div></div>')
            )
        )