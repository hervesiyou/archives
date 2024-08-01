from django.db import models
from arch_portal.domain.models.CONST_DATA import ASSO_CHOICES

class Association(models.Model):
    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Les Associations"
    
    db_table = "associations"
    nom = models.CharField(max_length=150)
    description = models.TextField( blank=True)
    type = models.CharField(
        max_length=50, 
        choices=ASSO_CHOICES,
        blank=True,null=1
    )
    def __str__(self):
        return self.nom
    
