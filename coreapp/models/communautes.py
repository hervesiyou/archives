from django.db import models
from coreapp.core.CONST_DATA import COM_CHOICES, REGIONS_CHOICES

class  Communautes(models.Model):
    class Meta:
        verbose_name = "Communauté"
        verbose_name_plural = " Les Communautés "
    
    nom = models.CharField(max_length=150)
    description = models.TextField( default="")
    superficie = models.CharField(max_length=50, default=0)
    histoire = models.TextField(default="", blank=True)
    geographie = models.TextField(default="", blank=True)
    origine = models.CharField(max_length=150, default="")
    type =  models.CharField(max_length=50, choices=COM_CHOICES,blank=True,null=1)
    region = models.CharField(max_length=50, choices=REGIONS_CHOICES,blank=True,null=1)
    
    chef = models.ForeignKey("Membres",on_delete=models.CASCADE, blank=True)
    
    def __str__(self):
        return self.nom