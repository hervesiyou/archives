from django.db import models

from arch_portal.domain.models.galerie import Galerie
from arch_portal.domain.models.association import Association
from arch_portal.domain import models as mod
import uuid
import secrets
import string
from django.utils.text import slugify

class Famille(models.Model):
    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Les Familles"
    
    db_table = "familles"
    nom = models.CharField(max_length=150)
    publique = models.BooleanField(default=False)
    description = models.TextField()
    histoire = models.TextField( null=True, blank=True)
    origine = models.TextField(  null=True, blank=True)
    urlgoogle = models.CharField( max_length=250, null=True, blank=True)
    type = models.CharField(max_length=50, blank=True)
    
    famille_mere = models.ForeignKey("Famille",on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ForeignKey("Image",on_delete=models.SET_NULL, null=True, blank=True)
    communaute = models.ForeignKey("Communaute",on_delete=models.SET_NULL, null=True, blank=True)
    chef = models.ForeignKey("Membre",on_delete=models.SET_NULL,related_name="mon_chef", null=True, blank=True)

    createur = models.ForeignKey("Membre",on_delete=models.SET_NULL,related_name="familles_creees", null=True, blank=True)

    associations = models.ManyToManyField(Association, related_name="association_familles", null=True, blank=True)
    galeries = models.ManyToManyField(Galerie, related_name="galeries_famille", null=True, blank=True)
    administrateurs = models.ManyToManyField("Membre", related_name="fam_admins", blank=True, null=True)

    code_unique = models.CharField( 
        max_length=40, 
        # unique=True, 
        editable=False, 
        db_index=True, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.nom

    def _generer_code_unique(self): 
        """ Génère un code lisible : NOM-XXXXXXXX Exemple : DUPONT-A7K92P4X Le nom permet d'identifier rapidement la famille. Le suffixe aléatoire garantit l'unicité pratique. """
        nom = (self.nom or "FAMILLE").strip()  
        nom_code = slugify(nom).replace("-", "").upper() 
        nom_code = nom_code[:12] 
        if not nom_code: 
            nom_code = "FAMILLE" 
        
        alphabet = string.ascii_uppercase + string.digits 
        suffixe = "".join( secrets.choice(alphabet) for _ in range(10) )  
        return f"{nom_code}-{suffixe}"

    def save(self, *args, **kwargs):
        if not self.code_unique:
            code = self._generer_code_unique()
            while Famille.objects.filter(code_unique=code).exists():
                code = self._generer_code_unique()
            self.code_unique = code

        super().save(*args, **kwargs)

    @property
    def membres(self):
        return self.membres_famille.all()

    @property
    def pages_famille(self):
        return self.pages_famille.all()
    
    def get_members(self):
        members = mod.Membre.objects.filter(familles=self.id)
        return members

    def get_membres(self):
        return self.membres_famille.all()

    def appartient(self, userid):
        
        member = mod.Membre.objects.filter(id=userid)
        # print( self.membres_famille.all() , member, userid, (member in self.membres_famille.all()) )
        if  member :
            return ( member in self.membres_famille.all() or (member in self.administrateurs.all() ))           
        else :
            return False 
        # return False

    def get_sous_familles(self):
        return mod.Famille.objects.filter(famille_mere=self.id)