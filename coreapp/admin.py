from django.contrib import admin

# Register your models here.
from coreapp.models.communautes import Communautes
from coreapp.models.familles import Familles
from coreapp.models.membres import Membres
from coreapp.models.associations import Associations
from coreapp.models.librairies import Librairies
from coreapp.models.livres import Livres
from coreapp.models.galeries import Galeries
from coreapp.models.images import Images
from coreapp.models.marches import Marches

admin.site.register(Communautes)
admin.site.register(Familles)
admin.site.register(Membres)
admin.site.register(Associations)
admin.site.register(Librairies)
admin.site.register(Livres)
admin.site.register(Galeries)
admin.site.register(Images)
admin.site.register(Marches)