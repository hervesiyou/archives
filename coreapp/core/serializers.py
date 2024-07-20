from rest_framework import routers, serializers, viewsets
from coreapp.models.communaute import Communaute
from libcore.models.librairie import Librairie
from coreapp.models import *

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