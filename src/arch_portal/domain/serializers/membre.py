from rest_framework import serializers
from arch_portal.domain.models import Membre

class MembreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membre
        fields = '__all__'