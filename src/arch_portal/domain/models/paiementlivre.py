# models.py
from django.db import models
from django.utils import timezone

from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.livre import Livre

class PaiementLivre(models.Model):
    acheteur = models.ForeignKey(  Membre, on_delete=models.CASCADE, related_name="paiements"  )
    livre = models.ForeignKey( Livre,  on_delete=models.CASCADE, related_name="paiements" )
    montant = models.DecimalField( max_digits=10, decimal_places=2 )
    date_paiement = models.DateTimeField(default=timezone.now)
    reference = models.CharField( max_length=100,  unique=True  )
    statut = models.CharField(
        max_length=20,
        choices=[("PAYE", "Payé"), ("EN_ATTENTE", "En attente")],
        default="PAYE"
    )

    class Meta:
        ordering = ["-date_paiement"]
        unique_together = ("acheteur", "livre")

    def __str__(self):
        return f"{self.acheteur} - {self.livre} - {self.montant}"
