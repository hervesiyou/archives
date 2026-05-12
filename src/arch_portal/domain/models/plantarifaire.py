from django.db import models 

class Plan(models.Model):
    nom = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=50, blank=True)
    appli = models.CharField(max_length=10, blank=True)

    nbcommunautes = models.CharField(max_length=10, blank=True, default=0)
    nbadministrateurs = models.CharField(max_length=10, blank=True, default=0)
    nbfamilles = models.CharField(max_length=10, blank=True, default=0)
    nblivres = models.CharField(max_length=10, blank=True, default=0)
    nbcagnotes = models.CharField(max_length=10, blank=True, default=0)
    nblibrairies = models.CharField(max_length=10, blank=True, default=0)

    avantages = models.TextField( blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    

    def __str__(self):
        return self.nom