
from django import forms
from arch_portal.domain.models.galerie import Galerie
class GalerieForm(forms.ModelForm):
    class Meta:
        model = Galerie
        exclude  = [""]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nom"].widget.attrs.update({"class":" form-control","title":"Nom de la galerie"}   )
        self.fields["description"].widget.attrs.update({"class":" form-control","title":"Description de la galerie"}   )
        
