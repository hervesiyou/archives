from django.db import models
from coreapp.core.CONST_DATA import LIB_CHOICES

class Librairies(models.Model):
    class Meta:
        verbose_name = "Librairie "
        verbose_name_plural = "  Les Librairies "
    
    nom = models.CharField(max_length=250)
    description = models.TextField()
   
    type = models.CharField(max_length=50, choices=LIB_CHOICES,blank=True,null=1)
    lieu = models.CharField(max_length=250, null=True)
    
    possesseur = models.ForeignKey("Membres", on_delete=models.CASCADE, null=True)
    livres = models.ManyToManyField("Livres",related_name="mes_livres", null=True, blank=True)
    
    def __str__(self): 
        return "{} ".format(str(self.nom).capitalize())
