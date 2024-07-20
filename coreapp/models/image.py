from django.db import models

 

class Image(models.Model):
    nom = models.CharField(max_length=50)
    galerie = models.ForeignKey("Galerie", on_delete=models.CASCADE,related_name="ma_galerie", null=True, blank=True)
    
    def __str__(self):
        return self.nom
    