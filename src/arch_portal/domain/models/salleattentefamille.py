from django.db import models
from .membre import Membre
from .famille import Famille
from arch_portal.domain.models.CONST_DATA import STATUTDEMANDE_CHOICES as STATUT_CHOICES

class SalleAttenteFamille(models.Model):
    class Meta:
        verbose_name = " Salle attente familles"
        unique_together = ('personne', 'famille')       

    personne = models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="demandes_acces")
    validateur = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="validateur_fam", null=True)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="demandes_acces")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    
    message = models.TextField(null=True, blank=True, help_text="Message du demandeur")
    message_reponse = models.TextField(null=True, blank=True, help_text="Réponse de l'administrateur")

    date_demande = models.DateField(auto_now=True)
    date_validation = models.DateField(null=True, blank=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.personne.nomcomplet} pour {self.famille.nom}'

    def approuver(self, validateur):
        self.statut = 'accepte'
        self.valide = True
        self.validateur = validateur
        self.date_validation = models.DateField(auto_now=True)
        self.save()

        self.personne.familles.add(self.famille)

        self.famille.membres_famille.add(self.personne)
        self.famille.save()

    def refuser(self, validateur,message=None):
        self.statut ="refuse"
        self.valide = False
        self.validateur = validateur
        self.date_validation = models.DateField(auto_now=True)
        if message:
            self.message_reponse = message
        self.save()