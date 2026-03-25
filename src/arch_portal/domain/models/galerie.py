 
from django.db import models 

class Galerie(models.Model):
    class Meta:
        verbose_name = "Galerie"
        verbose_name_plural = "Les Galeries"
    
    nom = models.CharField(max_length=250)
    description = models.TextField(null=True )
    images = models.ManyToManyField("Image", related_name="mes_images", blank=True)

    communaute = models.ForeignKey("Communaute", on_delete=models.CASCADE, blank=True, null=True, related_name="com_galerie")
    association = models.ForeignKey("Association", on_delete=models.CASCADE, blank=True, null=True, related_name="asso_galerie")
    famille = models.ForeignKey("Famille", on_delete=models.CASCADE, blank=True, null=True, related_name="fam_galerie")
    evenement = models.ForeignKey("Evenement", on_delete=models.CASCADE, blank=True, null=True, related_name="ev_galerie")


    def __str__(self):
        return self.nom
