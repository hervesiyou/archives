from django.contrib import admin

# Register your models here.
from coreapp.models.communaute import Communaute
from coreapp.models.famille import Famille
from coreapp.models.association import Association
from libcore.models.librairie import Librairie
from libcore.models.livre import Livre
from coreapp.models.membre import Membre
from coreapp.models.galerie import Galerie
from coreapp.models.image import Image
from coreapp.models.marche import Marche

admin.site.register(Communaute)
admin.site.register(Famille)
admin.site.register(Membre)
admin.site.register(Association)
admin.site.register(Librairie)
admin.site.register(Livre)
admin.site.register(Galerie)
admin.site.register(Image)
admin.site.register(Marche)