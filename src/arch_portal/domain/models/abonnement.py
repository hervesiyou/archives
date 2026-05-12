
from django.db import models
# from decimal import Decimal
# from django.utils import timezone
from datetime import timedelta, date 

class Abonnement(models.Model):
    
    code = models.CharField(max_length=50, blank=True)
    prix = models.IntegerField( blank=True)
     
    debut = models.DateTimeField(auto_now_add=True)
    fin = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    membre = models.ForeignKey("Membre", on_delete=models.CASCADE, related_name='abonnements')
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE, null=True, blank=True, related_name='abonnements')
    plan_appli = models.CharField(max_length=10, blank=True)
    # garde si on est obonement de librairie ou communauté
    type = models.CharField(max_length=10, blank=True) 
    duree =  models.IntegerField(default=365)

    def __str__(self):
        return f"{self.membre.nomcomplet}  -{self.plan_appli}"

    def save(self, *args, **kwargs):
        # Calculer la date d'expiration en fonction de la durée du forfait
        if not self.fin:
            nouvelle_date = date(self.debut.year + int(self.duree), self.debut.month, self.debut.day)

            while nouvelle_date.month > 12:
                nouvelle_date = date(nouvelle_date.year + 1, nouvelle_date.month - 12, nouvelle_date.day)

            try:
                nouvelle_date = date(nouvelle_date.year, nouvelle_date.month, self.debut.day)
            except ValueError:
                import calendar
                dernier_jour = calendar.monthrange(nouvelle_date.year, nouvelle_date.month)[1]
                nouvelle_date = date(nouvelle_date.year, nouvelle_date.month, dernier_jour)
                # print("Attention : Dépassement de jour. Ajusté au dernier jour du mois.")
 
            self.fin = nouvelle_date 
        super().save(*args, **kwargs)
