from django.db import models
# from .wallet import Wallet
from arch_portal.domain.models.CONST_DATA import SEX_CHOICES, ETATCIVIL_CHOICES, TYPE_MEMBER_CHOICES, GENERATIONS
from .famille import Famille
from .association import Association
from .image import Image
from .galerie import Galerie
from .role import Role
from .message import Message
from .communaute import Communaute
from .badge import Badge

class Membre(models.Model):
    class Meta:
        verbose_name = " Membre"
        verbose_name_plural = "Les Membres"
    
    photo = models.ForeignKey("Image", related_name="membre_photo", on_delete=models.SET_NULL, null=True, blank=True)

    description = models.CharField(max_length=1000, null=True, blank=True)
    nomcomplet = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    pwd = models.CharField(max_length=300)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    etatvalidation = models.BooleanField(default=False,null=True)
    token = models.CharField( blank=True,null=True,max_length=100, default="")
    dateinscription = models.DateTimeField(null=True,auto_now_add=True)
    
    generation =  models.CharField(max_length=50, choices=GENERATIONS,blank=True,null=1)
    type =  models.CharField(max_length=50, choices=TYPE_MEMBER_CHOICES,blank=True,null=1)
    sexe =  models.CharField(max_length=50, choices=SEX_CHOICES,blank=True,null=1)
     
    datenaissance = models.CharField(max_length=50, null=True)
    lieunaissance = models.CharField(max_length=50, null=True, blank=True)
    residence = models.CharField(max_length=150, null=True, blank=True)
    etatcivil = models.CharField(max_length=50, choices=ETATCIVIL_CHOICES, null=True, blank=True)
    nbenfant = models.IntegerField(default=0)
    notabilite = models.CharField(max_length=250, null=True, blank=True)
    education = models.CharField(max_length=250, null=True, blank=True)
    diplomes = models.CharField(max_length=250, null=True, blank=True)
    profession = models.CharField(max_length=150, null=True, blank=True)
    
    messages = models.ManyToManyField(Message,related_name="membres_message", blank=True)
    familles = models.ManyToManyField(Famille,related_name="membres_famille", null=True)
    associations = models.ManyToManyField(Association, related_name="membres_association", null=True, blank=True)
    images = models.ManyToManyField(Image, null=True, blank=True)
    communautes = models.ManyToManyField(Communaute, related_name="membres_communaute", null=True, blank=True)
    galeries = models.ManyToManyField(Galerie, related_name="mes_galeries", null=True, blank=True)
    approbateurs = models.ManyToManyField("self", null=True, blank=True)
    # wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, null=True, blank=True)
    
    pere = models.CharField(max_length=150,null=True, blank=True)
    mere = models.CharField(max_length=150,null=True, blank=True)

    nompere = models.ForeignKey('self',on_delete=models.SET_NULL, related_name="papa",null=True, blank=True)
    nommere = models.ForeignKey('self',on_delete=models.SET_NULL,related_name="mama",null=True, blank=True)
    vivant = models.BooleanField(default=True)
    datedeces = models.CharField(max_length=50, null=True, blank=True)

    role = models.ManyToManyField(  Role, null=True, blank=True )

    badges = models.ManyToManyField(  Badge, blank=True,  related_name="membres")
       
    def save(self, *args, **kwargs): 

        if self.pere != None and self.mere != None:
            if len(self.pere)<3 and len(self.mere)<3:
                if len(self.nompere.nomcomplet)<3 and len(self.nommere.nomcomplet)<3:
                    # print("merci de choisir les parents")
                    raise ValueError("Merci de fournir les parents de ce membre")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nomcomplet

    def total_contributions_et_dons(self):
        return self.contributions.count() + self.dons_effectues.count()

    def montant_total_contributions(self):
        total = self.contributions.aggregate( total=models.Sum("montant") )["total"]
        total_don = self.dons_effectues.aggregate( total=models.Sum("montant") )["total"]

        return (total + total_don ) or 0

    def jappartient_asso(self,asso):
        return ( asso in self.associations.all() )
           
    def get_rights(self):
        return [perm.nom for role in self.role.all() for perm in role.permissions.all() ]
  
    def get_familles(self):
        # return self.librairies.all().first().nom
        return [lib.nom for lib in self.familles.all()]
    
    def appartient_a_famille(self, famille_or_id):
        """Vérifie si le membre appartient à une famille (objet ou ID)"""
        if famille_or_id is None:
            return False
        if isinstance(famille_or_id, int):
            return self.familles.filter(id=famille_or_id).exists()
        return self.familles.filter(id=famille_or_id.id).exists()

    def appartient_a_communaute(self, com_or_id):
        """Vérifie si le membre appartient à une Communaute (objet ou ID)"""
        if com_or_id is None:
            return False
        if isinstance(com_or_id, int):
            return self.communautes.filter(id=com_or_id).exists()
        return self.communautes.filter(id=com_or_id.id).exists()
    
    def appartient_a_association(self, ass_or_id):
        """Vérifie si le membre appartient à une Association (objet ou ID)"""
        if ass_or_id is None:
            return False
        if isinstance(ass_or_id, int):
            return self.associations.filter(id=ass_or_id).exists()
        return self.associations.filter(id=ass_or_id.id).exists()


