from django.db import models

from arch_portal.domain.models.CONST_DATA import LIV_CHOICES
class Livre(models.Model):
    class Meta:
        verbose_name = "  Livre de bibliotheque "
        verbose_name_plural = " Les  Livres"
    
    db_table = "livres"
    nom = models.CharField(max_length=150)
    description = models.TextField(null=True)
    auteur = models.CharField(max_length=250)
    domaine = models.CharField(max_length=250, null=True, blank=True)
    prix = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=LIV_CHOICES,blank=True)
    librairies = models.ManyToManyField("Librairie",related_name="mes_librairies", null=True)
    def __str__(self):
        return f"{self.nom}, {self.auteur}"

    def get_librairies(self):
        return self.librairies.all().first().nom
        # return [lib.nom for lib in self.librairies.all()]