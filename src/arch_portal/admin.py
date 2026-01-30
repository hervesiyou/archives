from django.contrib import admin

# Register your models here.
from arch_portal.domain.models.categorielivre import Categorie
from arch_portal.domain.models.wallet import Wallet
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.association import Association
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.galerie import Galerie
from arch_portal.domain.models.image import Image
from arch_portal.domain.models.contact import Contact
from arch_portal.domain.models.marche import Marche
from arch_portal.domain.models.commandelivre import CommandeLivre
from arch_portal.domain.models import Role,Permission
from arch_portal.domain.models.evenement import Evenement
from arch_portal.domain.models.abonnement import Abonnement
from arch_portal.domain.models.plantarifaire import Plan
from arch_portal.domain.models.message import Message
from arch_portal.domain.models.salleattentefamille import SalleAttenteFamille
from arch_portal.domain.models.salleattentecommunaute import SalleAttenteCommunaute
from arch_portal.domain.models.salleattenteassociation import SalleAttenteAssociation
from arch_portal.domain.models.paiementlivre import PaiementLivre
from arch_portal.domain.models.notationlivre import NotationLivre

admin.site.register(Communaute)
admin.site.register(Contact)
admin.site.register(Categorie)
admin.site.register(Famille)
admin.site.register(Membre)
admin.site.register(Association)
admin.site.register(Librairie)
admin.site.register(Livre)
admin.site.register(Galerie)
admin.site.register(Image)
admin.site.register(Marche)
admin.site.register(CommandeLivre)
admin.site.register(Evenement)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Abonnement)
admin.site.register(Plan)
admin.site.register(SalleAttenteCommunaute)
admin.site.register(SalleAttenteAssociation)
admin.site.register(SalleAttenteFamille)
admin.site.register(Message)
admin.site.register(Wallet)
admin.site.register(PaiementLivre)
admin.site.register(NotationLivre)
