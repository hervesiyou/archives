
from django import forms
from arch_portal.domain.models.image import Image
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"
