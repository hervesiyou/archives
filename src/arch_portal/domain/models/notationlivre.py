
# models.py
from django.db import models
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.membre import Membre


class NotationLivre(models.Model):
    livre = models.ForeignKey( Livre, on_delete=models.CASCADE, related_name="notations"  )
    auteur = models.ForeignKey( Membre, on_delete=models.CASCADE, related_name="notations" )
    note = models.PositiveSmallIntegerField()  # 1 à 5
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("livre", "auteur")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.livre.nom} - {self.note}⭐"
