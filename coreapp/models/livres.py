from django.db import models
# from core.CONST_DATA import *

class Livres(models.Model):
    class Meta:
        verbose_name = "  Livre de bibliotheque "
        verbose_name_plural = " Les  Livres"
    
    nom = models.CharField(max_length=150)
    description = models.TextField(null=True)
    auteur = models.CharField(max_length=250)
    domaine = models.CharField(max_length=250, null=True, blank=True)
    prix = models.IntegerField(default=0)
    
    librairies = models.ManyToManyField("Librairies",related_name="mes_librairies", null=True )
    
    def __str__(self):
        return self.nom
