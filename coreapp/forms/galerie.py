
from django import forms
from coreapp.models.galerie import Galerie


class GalerieForm(forms.ModelForm):
    
    class Meta:
        model = Galerie
        exclude  = [""]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs.update({"class":"bg-info","title":"Une description"}   )
        
