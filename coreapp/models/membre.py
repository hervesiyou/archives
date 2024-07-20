from django.db import models
from coreapp.core.CONST_DATA import SEX_CHOICES, ETATCIVIL_CHOICES, TYPE_MEMBER_CHOICES
 
class Membre(models.Model):
    class Meta:
        verbose_name = " Membre"
        verbose_name_plural = "Les Membres"
    
    nomcomplet = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)
    etatvalidation = models.BooleanField(default=0,null=True)
    dateinscription = models.DateTimeField(null=True)
    
    type =  models.CharField(max_length=50, choices=TYPE_MEMBER_CHOICES,blank=True,null=1)
    sexe =  models.CharField(max_length=50, choices=SEX_CHOICES,blank=True,null=1)
     
    datenaissance = models.CharField(max_length=50, null=True)
    lieunaissance = models.CharField(max_length=50, null=True, blank=True)
    residence = models.CharField(max_length=150, null=True, blank=True)
    etatcivil = models.CharField(max_length=50, choices=ETATCIVIL_CHOICES, null=True)
    nbenfant = models.IntegerField(default=0)
    notabilite = models.CharField(max_length=250, null=True, blank=True)
    education = models.CharField(max_length=250, null=True, blank=True)
    diplomes = models.CharField(max_length=250, null=True, blank=True)
    profession = models.CharField(max_length=150, null=True, blank=True)
    
    familles = models.ManyToManyField("Famille",related_name="mes_familles", null=True)
    approbateurs = models.ManyToManyField("Membre", null=True, blank=True)
    associations = models.ManyToManyField("Association", null=True, blank=True)
    images = models.ManyToManyField("Image", null=True, blank=True)
    galeries = models.ManyToManyField("Galerie", related_name="mes_galeries", null=True, blank=True)
    
    pere = models.CharField(max_length=150)
    mere = models.CharField(max_length=150)
    vivant = models.BooleanField(default=True)
    datedeces = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.nomcomplet

