from libcore.models.livre import Livre
from django.forms import ModelForm
class LivreForm(ModelForm):
    
    class Meta:
        model = Livre
        fields = "__all__"