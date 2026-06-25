from django.db import models
from arch_portal.domain.models.CONST_DATA import ASSO_CHOICES
from arch_portal.domain import models as modeles

class Association(models.Model):
    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Les Associations"
    
    db_table = "associations"
    nom = models.CharField(max_length=150)
    publique = models.BooleanField(default=True)
    description = models.TextField( blank=True)
    adhesion = models.TextField( blank=True)
    contact = models.TextField( blank=True)

    createur = models.ForeignKey("Membre", on_delete=models.SET_NULL,blank=True, null=True, related_name="associations_cree")

    famille = models.ForeignKey("Famille", on_delete=models.SET_NULL,blank=True, null=True)
    communaute = models.ForeignKey("Communaute", on_delete=models.SET_NULL,blank=True, null=True)
    localisation = models.TextField( blank=True)

    administrateurs = models.ManyToManyField("Membre", related_name="asso_admins", blank=True, null=True)
    type = models.CharField( max_length=50, choices=ASSO_CHOICES, blank=True,null=1 )

    def __str__(self):
        return self.nom
    
    def userid_appartient(self, userid ):
        for m in self.membres_association.all():
            if( userid == m.id):
                return True
        return False
    
