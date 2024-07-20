from libcore.models.librairie import Librairie
from django.forms import ModelForm
class LibrairieForm(ModelForm):
    
    class Meta:
        model = Librairie
        fields = "__all__"