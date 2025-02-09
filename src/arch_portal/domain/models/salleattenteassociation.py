from django.db import models
from .membre import Membre
from .association import Association

class SalleAttenteAssociation(models.Model):
    class Meta:
        verbose_name = " Salle attente association"

    personne = models.ForeignKey(Membre, on_delete=models.CASCADE)
    validateur = models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="validateur_asso", null=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    date_demande = models.DateField(auto_now=True)
    date_validation = models.DateField(null=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.personne.nomcomplet} pour {self.association.nom}'