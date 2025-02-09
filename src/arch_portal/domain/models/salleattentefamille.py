from django.db import models
from .membre import Membre
from .famille import Famille

class SalleAttenteFamille(models.Model):
    class Meta:
        verbose_name = " Salle attente familles"
        

    personne = models.ForeignKey(Membre, on_delete=models.CASCADE)
    validateur = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="validateur_fam", null=True)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)
    date_demande = models.DateField(auto_now=True)
    date_validation = models.DateField(null=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.personne.nomcomplet} pour {self.famille.nom}'