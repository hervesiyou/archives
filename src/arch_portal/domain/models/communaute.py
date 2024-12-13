from django.db import models
from arch_portal.domain.models.CONST_DATA import COM_CHOICES, REGIONS_CHOICES

from arch_portal.domain import models as modeles


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
    listerois = models.CharField(max_length=150, default="")
    type =  models.CharField(max_length=50, choices=COM_CHOICES,blank=True,null=1)
    region = models.CharField(max_length=50, choices=REGIONS_CHOICES,blank=True,null=1)
    chef = models.ForeignKey("Membre",on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nom

    def get_evenements(self):
        return modeles.Evenement.objects.filter(communaute=self.id)

    def get_familles(self):
        return modeles.Famille.objects.filter(communaute=self.id)

    def get_associations(self):
        return modeles.Association.objects.filter(communaute=self.id)