from django.db import models 
from arch_portal.domain.models.CONST_DATA import LIB_CHOICES
from arch_portal.domain.models.publicite import Tag

class Librairie(models.Model):
    class Meta:
        verbose_name = "Librairie "
        verbose_name_plural = "  Les Librairies "
    
    db_table ="librairies"
    nom = models.CharField(max_length=250)
    description = models.TextField()
    
    tags = models.ManyToManyField( Tag, related_name="librairies", blank=True, help_text=( "Centres d'intérêt / types de librairies ciblés. "  "Laisser vide = publicité générique affichée en l'absence de correspondance."  ),  )

    type = models.CharField(max_length=50, choices=LIB_CHOICES,blank=True)
    lieu = models.CharField(max_length=250, null=True)    
    possesseur = models.ForeignKey("Membre", on_delete=models.CASCADE, related_name="librairies", null=True)
    image = models.ForeignKey("Image",on_delete=models.SET_NULL, null=True, blank=True)
    # livres = models.ManyToManyField("Livre",related_name="mes_livres",  blank=True)
    
    def __str__(self): 
        return "{} ".format(str(self.nom).capitalize())
    
    @property
    def nombre_livres(self):
        return self.livres.count()
