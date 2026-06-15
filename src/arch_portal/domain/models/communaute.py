from django.db import models
from arch_portal.domain.models.CONST_DATA import COM_CHOICES, REGIONS_CHOICES
from django.utils.translation import gettext_lazy as _
from arch_portal.domain import models as modeles
from .geographie import LieuGeographique
from .histoire import MiniHistoire
from .roi import Rois


class  Communaute(models.Model):
    class Meta:
        verbose_name = "Communauté"
        verbose_name_plural = " Les Communautés "
    
    db_table = "communautes"
    nom = models.CharField(max_length=150)
    publique = models.BooleanField(default=True)
    description = models.TextField( default="")
    superficie = models.CharField(max_length=50, default=0)
    histoire = models.TextField(default="", blank=True)
    histoires = models.ManyToManyField(MiniHistoire, null=True, blank=True, related_name="communaute_histoires")

    legende_fondatrice = models.TextField( blank=True,  verbose_name=_(" Légende de fondation"), help_text=_("Récit mythique ou traditionnel de l'origine") )
    histoire_detaillee = models.TextField( blank=True, verbose_name=_("Histoire détaillée"), help_text=_("Événements historiques, évolutions, dates clés") )
    image = models.ForeignKey("Image",on_delete=models.SET_NULL, null=True, blank=True)
    # latitude = models.TextField(default="", blank=True)
    # geographie = models.TextField(default="", blank=True)
    geographie = models.ForeignKey(LieuGeographique, on_delete=models.CASCADE, blank=True, null=True, related_name="communaute_geographie")

    origine = models.CharField(max_length=150, default="")
    listerois = models.CharField(max_length=150, default="", null=True, blank=True)
    type =  models.CharField(max_length=50, choices=COM_CHOICES,blank=True,null=1)
    region = models.CharField(max_length=50, choices=REGIONS_CHOICES,blank=True,null=1)
    chef = models.ForeignKey("Membre",on_delete=models.CASCADE, blank=True, null=True)
    administrateurs = models.ManyToManyField("Membre", related_name="com_admins", blank=True, null=True)
    rois = models.ManyToManyField(Rois, related_name="com_rois", blank=True, null=True)

    def __str__(self):
        return self.nom

    def get_evenements(self):
        return modeles.Evenement.objects.filter(communaute=self.id)

    def get_familles(self):
        return modeles.Famille.objects.filter(communaute=self.id)

    def get_associations(self):
        return modeles.Association.objects.filter(communaute=self.id)
        # Optionnel : méthode pratique

    def get_rois_chronologiques(self):
        return self.rois.order_by('annee_debut')  
    
    def get_formations(self):
        return self.formations.all()

    def get_articles(self):
        return self.articles.all().order_by('-dateajout')