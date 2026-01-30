# models.py
from django.db import models
from django.utils import timezone

from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.CONST_DATA import STATUTS

class PaiementLivre(models.Model):

    acheteur = models.ForeignKey(  Membre, on_delete=models.CASCADE, related_name="paiements"  )
    recepteur = models.ForeignKey( Membre, on_delete=models.CASCADE, related_name="paiements_recus", null=True, blank=True )

    livre = models.ForeignKey( Livre,  on_delete=models.CASCADE, related_name="paiements" )
    montant = models.DecimalField( max_digits=10, decimal_places=2 )
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now)
    
    reference = models.CharField( max_length=100,  unique=True  )
    statut = models.CharField( max_length=20, choices=STATUTS,  default="PAYE"  )

    reference_remboursement = models.CharField( max_length=100,  null=True, blank=True ) 
    date_remboursement = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date_paiement"]
        unique_together = ("acheteur", "livre")

    def __str__(self):
        return f"{self.acheteur} - {self.livre} - {self.montant}"
