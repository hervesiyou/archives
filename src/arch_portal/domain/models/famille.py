from django.db import models

from arch_portal.domain.models.galerie import Galerie
from arch_portal.domain.models.association import Association
from arch_portal.domain import models as mod


class Famille(models.Model):
    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Les Familles"
    
    db_table = "familles"
    nom = models.CharField(max_length=150)
    publique = models.BooleanField(default=True)
    description = models.TextField()
    histoire = models.TextField( null=True, blank=True)
    origine = models.TextField(  null=True, blank=True)
    urlgoogle = models.CharField( max_length=250, null=True, blank=True)
    type = models.CharField(max_length=50, blank=True)
    
    famille_mere = models.ForeignKey("Famille",on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ForeignKey("Image",on_delete=models.SET_NULL, null=True, blank=True)
    communaute = models.ForeignKey("Communaute",on_delete=models.SET_NULL, null=True, blank=True)
    chef = models.ForeignKey("Membre",on_delete=models.SET_NULL,related_name="mon_chef", null=True, blank=True)
    associations = models.ManyToManyField(Association, related_name="association_familles", null=True, blank=True)
    galeries = models.ManyToManyField(Galerie, related_name="galeries_famille", null=True, blank=True)
    administrateurs = models.ManyToManyField("Membre", related_name="fam_admins", blank=True, null=True)

    def __str__(self):
        return self.nom
    
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
        
        member = mod.Membre.objects.get(id=userid)
        if  member :
            if( member in self.membres_famille.all() ):
                return True 
            else :
                return False 
        return False

    def get_sous_familles(self):
        return mod.Famille.objects.filter(famille_mere=self.id)