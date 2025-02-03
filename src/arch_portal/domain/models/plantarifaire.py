from django.db import models 

class Plan(models.Model):
    nom = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=50, blank=True)
    appli = models.CharField(max_length=10, blank=True)
    avantages = models.TextField( blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    

    def __str__(self):
        return self.nom