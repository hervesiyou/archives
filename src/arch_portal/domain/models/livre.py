from django.db import models

from arch_portal.domain.models.categorielivre import Categorie
from .image import Image
from .membre import Membre
import random
from arch_portal.domain.models.CONST_DATA import LIV_CHOICES

class Livre(models.Model):
    
    class Meta:
        verbose_name = "  Livre de bibliotheque "
        verbose_name_plural = " Les  Livres"
    
    db_table = "livres"
    nom = models.CharField(max_length=150)
    description = models.TextField(null=True)
    auteur = models.CharField(max_length=250)
    stock = models.IntegerField(default=1,null=True)

    isbn = models.CharField(max_length=250, null=True, blank=True)
    langue = models.CharField(max_length=250, null=True, blank=True)
    # cover_image = models.ImageField(upload_to='couvertures/')
    file = models.FileField(upload_to='livres/',null=True, blank=True)
    images = models.ManyToManyField(Image, null=True, blank=True)

    domaine = models.CharField(max_length=250, null=True, blank=True)
    prix = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=LIV_CHOICES,blank=True)
    librairies = models.ManyToManyField("Librairie",related_name="livres", null=True)

    proprietaire = models.ForeignKey( Membre,  on_delete=models.SET_NULL,  null=True,  blank=True,  related_name="livres_possedes"  )
    anciens_proprietaires = models.ManyToManyField(  Membre, blank=True,  related_name="livres_deja_possedes" )
    categorie = models.ForeignKey( Categorie,   on_delete=models.SET_NULL,  null=True,  blank=True,  related_name="livres")

    def __str__(self):
        return f"{self.nom}, {self.auteur}  (ISBN: {self.isbn})"
    
    def moyenne_notes(self):
        return self.notations.aggregate(avg=models.Avg("note"))["avg"] or 0

    def total_notes(self):
        return self.notations.count()


    def generer_isbn(self):
        """Génère un code ISBN-13 aléatoire valide."""
        prefixe_978 = "978"
        groupe = str(random.randint(0, 999))  # Code de groupe (peut varier)
        editeur = str(random.randint(0, 99999)) # Code d'éditeur (peut varier)
        publication = str(random.randint(0, 999999)) # Code de publication

        base = f"{prefixe_978}{groupe.zfill(3)}{editeur.zfill(5)}{publication.zfill(6)}"

        # Calcul du chiffre de contrôle (algorithme ISBN-13)
        somme = 0
        for i, chiffre in enumerate(base):
            poids = 3 if (i + 1) % 2 == 0 else 1
            somme += int(chiffre) * poids

        chiffre_controle = (10 - (somme % 10)) % 10
        return f"{base}{chiffre_controle}"

    def get_librairies(self):
        return self.librairies.all().first().nom
        # return [lib.nom for lib in self.librairies.all()]
    
    def save(self, *args, **kwargs):
        """Génère un ISBN s'il n'en existe pas avant la sauvegarde."""
        if not self.isbn:
            self.isbn = self.generer_isbn()
        super().save(*args, **kwargs)