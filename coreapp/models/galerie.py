from django.db import models
from django import forms


class Galerie(models.Model):
    class Meta:
        verbose_name = "Galerie"
        verbose_name_plural = "Les Galeries"
    
    nom = models.CharField(max_length=250)
    description = models.TextField(null=True )
    images = models.ManyToManyField("Image", related_name="mes_images", blank=True)
    
    def __str__(self):
        return self.nom
