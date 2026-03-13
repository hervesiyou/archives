
from django import forms
from arch_portal.domain.models.image import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"

# ImageFormSet = forms.inlineformset_factory(
#     Image, form=ImageForm, extra=3, can_delete=True
# )

# ImageFormSet = forms.inlineformset_factory(
#     Image,
#     fields=('fichier', 'legende'),      # champs que tu veux éditer
#     extra=1,                            # 1 ligne vide pour ajouter une nouvelle image
#     can_delete=True,                    # permet de cocher "supprimer"
#     widgets={
#         'fichier': forms.FileInput(attrs={'class': 'form-control'}),
#         'legende': forms.TextInput(attrs={'class': 'form-control'}),
#     }
# )
