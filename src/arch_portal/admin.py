from django.contrib import admin

# Register your models here.
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.famille import Famille
from arch_portal.domain.models.association import Association
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models.livre import Livre
from arch_portal.domain.models.membre import Membre
from arch_portal.domain.models.galerie import Galerie
from arch_portal.domain.models.image import Image
from arch_portal.domain.models.marche import Marche
from arch_portal.domain.models.commandelivre import CommandeLivre

from arch_portal.domain.models.evenement import Evenement

admin.site.register(Communaute)
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
