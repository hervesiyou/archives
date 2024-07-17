from django.db import models
from coreapp.core.CONST_DATA import ASSO_CHOICES

class Associations(models.Model):
    class Meta:
        verbose_name = "  Association"
        verbose_name_plural = "Les Associations"
    
    nom = models.CharField(max_length=150)
    description = models.TextField( blank=True)
    type = models.CharField(max_length=50, choices=ASSO_CHOICES,blank=True,null=1)
    
    def __str__(self):
        return self.nom
    
