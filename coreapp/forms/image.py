
from django import forms
from coreapp.models.image import Image


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = "__all__"
