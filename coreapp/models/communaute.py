from django.db import models
from coreapp.models.membre import Membre
from coreapp.core.CONST_DATA import COM_CHOICES, REGIONS_CHOICES

class  Communaute(models.Model):
    class Meta:
        verbose_name = "Communauté"
        verbose_name_plural = " Les Communautés "
    
    db_table = "communautes"
    nom = models.CharField(max_length=150)
    description = models.TextField( default="")
    superficie = models.CharField(max_length=50, default=0)
    histoire = models.TextField(default="", blank=True)
    geographie = models.TextField(default="", blank=True)
    origine = models.CharField(max_length=150, default="")
    type =  models.CharField(max_length=50, choices=COM_CHOICES,blank=True,null=1)
    region = models.CharField(max_length=50, choices=REGIONS_CHOICES,blank=True,null=1)
    chef = models.ForeignKey("coreapp.Membre",on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.nom