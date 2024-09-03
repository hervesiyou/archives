from django.db import models
from arch_portal.domain.models.CONST_DATA import ASSO_CHOICES
from arch_portal.domain import models as modeles

class Association(models.Model):
    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Les Associations"
    
    db_table = "associations"
    nom = models.CharField(max_length=150)
    description = models.TextField( blank=True)
    adhesion = models.TextField( blank=True)
    contact = models.TextField( blank=True)
    communaute = models.ForeignKey("Communaute", on_delete=models.SET_NULL, null=True)
    localisation = models.TextField( blank=True)
    type = models.CharField(
        max_length=50, 
        choices=ASSO_CHOICES,
        blank=True,null=1
    )
    def __str__(self):
        return self.nom
    
