
from django.db import models
# from core.CONST_DATA import *

class Marches(models.Model):
    class Meta:
        verbose_name = "  Marché "
        verbose_name_plural = "  Nos Marchés  "
    
    nom = models.CharField(max_length=250)
    description = models.TextField() 
    lien = models.CharField(max_length=250, null=True)
    
    possesseur = models.ForeignKey("Membres", on_delete=models.CASCADE, null=True, blank=True)
   
    
    def __str__(self):
        return self.nom