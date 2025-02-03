

from django.db import models
from django.utils import timezone

class Abonnement(models.Model):
    
    code = models.CharField(max_length=50, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
     
    debut = models.DateTimeField(auto_now_add=True)
    fin = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    membre = models.OneToOneField("Membre", on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)

    duree =  models.IntegerField(default=365)

    def __str__(self):
        return f"{self.membre.nomcomplet} - {self.plan.nom}"

    def save(self, *args, **kwargs):
        # Calculer la date d'expiration en fonction de la durée du forfait
        if not self.fin:
            self.prix = self.plan.prix  * (self.duree / 365)
            self.fin = self.debut + timezone.timedelta(days=self.plan.duree)
        super().save(*args, **kwargs)
