from django.db import models 
from arch_portal.domain.models.CONST_DATA import LIB_CHOICES

class Librairie(models.Model):
    class Meta:
        verbose_name = "Librairie "
        verbose_name_plural = "  Les Librairies "
    
    db_table ="librairies"
    nom = models.CharField(max_length=250)
    description = models.TextField()
   
    type = models.CharField(max_length=50, choices=LIB_CHOICES,blank=True)
    lieu = models.CharField(max_length=250, null=True)
    
    possesseur = models.ForeignKey("Membre", on_delete=models.CASCADE, null=True)
    livres = models.ManyToManyField("Livre",related_name="mes_livres", null=True, blank=True)
    
    def __str__(self): 
        return "{} ".format(str(self.nom).capitalize())
