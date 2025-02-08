from django.db import models
from .membre import Membre
from .communaute import Communaute

class SalleAttenteCommunaute(models.Model):
    class Meta:
        verbose_name = " Salle attente communaute"
        

    personne = models.ForeignKey(Membre, on_delete=models.CASCADE)
    validateur = models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="validateur", null=True)
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    date_demande = models.DateField(auto_now=True)
    date_validation = models.DateField(null=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.personne.nomcomplet} pour {self.communaute.nom}'