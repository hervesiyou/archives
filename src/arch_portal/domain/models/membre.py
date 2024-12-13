from django.db import models
from arch_portal.domain.models.CONST_DATA import SEX_CHOICES, ETATCIVIL_CHOICES, TYPE_MEMBER_CHOICES
from .famille import Famille
from .association import Association
from .image import Image
from .galerie import Galerie
from .role import Role

class Membre(models.Model):
    class Meta:
        verbose_name = " Membre"
        verbose_name_plural = "Les Membres"
    
    nomcomplet = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    pwd = models.CharField(max_length=300)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
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
    
    familles = models.ManyToManyField(Famille,related_name="mes_familles", null=True)
    associations = models.ManyToManyField(Association, null=True, blank=True)
    images = models.ManyToManyField(Image, null=True, blank=True)
    galeries = models.ManyToManyField(Galerie, related_name="mes_galeries", null=True, blank=True)
    approbateurs = models.ManyToManyField("self", null=True, blank=True)
    
    pere = models.CharField(max_length=150,null=True, blank=True)
    mere = models.CharField(max_length=150,null=True, blank=True)
    nompere = models.ForeignKey('self',on_delete=models.SET_NULL, related_name="papa",null=True, blank=True)
    nommere = models.ForeignKey('self',on_delete=models.SET_NULL,related_name="mama",null=True, blank=True)
    vivant = models.BooleanField(default=True)
    datedeces = models.CharField(max_length=50, null=True, blank=True)

    role = models.ManyToManyField(
        Role
    )

    def save(self, *args, **kwargs):
        if len(self.pere)<3 and len(self.mere)<3:
            if len(self.nompere.nomcomplet)<3 and len(self.nommere.nomocomplet)<3:
                print("merci de choisir les parents")
                raise ValueError("Merci de fournir les parents de ce membre")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nomcomplet

    def get_rights(self):
        return [perm.nom for role in self.role.all() for perm in role.permissions.all() ]
    
    def get_familles(self):
        # return self.librairies.all().first().nom
        return [lib.nom for lib in self.familles.all()]


