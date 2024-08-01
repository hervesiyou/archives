from rest_framework import routers, serializers, viewsets
from arch_portal.domain.models.communaute import Communaute
from arch_portal.domain.models.librairie import Librairie
from arch_portal.domain.models import *

class LibrairiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Librairie
        fields =["id", "nom", "description", "type", "lieu"]
        
class CommunautesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Communaute
        fields = ["id", "nom", "description","type", "superficie"]
        
class MembresSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Membre
        fields = ["id", "nomcomplet", "sexe", "pere"]