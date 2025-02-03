
from django import forms
from arch_portal.domain.models.image import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"

# ImageFormSet = forms.inlineformset_factory(
#     Image, form=ImageForm, extra=3, can_delete=True
# )
