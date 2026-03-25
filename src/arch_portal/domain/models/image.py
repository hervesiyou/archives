from django.db import models
from PIL import Image as PILImage 
# import os
import PIL
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Image(models.Model):
    
    nom = models.CharField(max_length=50)
    fichier = models.ImageField(upload_to='book_images/' , null=True, blank=True)
    galerie = models.ForeignKey("Galerie", on_delete=models.CASCADE,related_name="ma_galerie", null=True, blank=True)
    sonlivre = models.ForeignKey("Livre", on_delete=models.CASCADE,related_name="sonlivre", null=True, blank=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        # Appeler la méthode save() du parent
        super().save(*args, **kwargs)
        # Ouvrir l'image avec Pillow
        img = PILImage.open(self.fichier.path)

        # Redimensionner l'image (par exemple, 800x800)
        if img.height > 2800 or img.width > 2800:
            output_size = (1024, 800)
            img.thumbnail(output_size, PIL.Image.LANCZOS)

        # Compresser l'image (qualité de 85%)
        img.save(self.fichier.path, quality=85)
    