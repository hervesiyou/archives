from django.db import models 

class Plan(models.Model):
    nom = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=50, blank=True)
    appli = models.CharField(max_length=10, blank=True)

    nbcommunautes = models.CharField(max_length=10, blank=True, default=0)
    nbadministrateurs = models.CharField(max_length=10, blank=True, default=1)
    nbfamilles = models.CharField(max_length=10, blank=True, default=1)
    nblivres = models.CharField(max_length=10, blank=True, default=1)
    nbcagnotes = models.CharField(max_length=10, blank=True, default=1)
    nblibrairies = models.CharField(max_length=10, blank=True, default=0)

    nbprojets = models.CharField(max_length=10, blank=True, default=0)
    nbevenements = models.CharField(max_length=10, blank=True, default=0)
    nbassociations = models.CharField(max_length=10, blank=True, default=1)
    
    nbevenements = models.CharField(max_length=10, blank=True, default=1)

    avantages = models.TextField( blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True)   

    is_default=models.BooleanField(default=False, verbose_name="Plan par defaut")

    def __str__(self):
        return self.nom

    class Meta: 
        verbose_name = "Plan tarifaire"
        verbose_name_plural = "Les Plans tarifaire"
    @classmethod
    def plan_default(cls):
        plan, created= cls.objects.get_or_create(
            is_default=True,
            defaults={
                "nom":"Plan Gratuit",
                "code":"GRATUIT",
                "prix":0,
                "avantages":"Plan Gratuit offert de base",
            }
        )
        return plan

    def save(self, *args, **kwargs):
        if self.is_default:
            Plan.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)