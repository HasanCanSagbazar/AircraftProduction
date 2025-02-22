from rest_framework import serializers
from .models import UavsAssembly, AssemblyPart
from parts.models import Part
from uavs.models import Uavs
from teams.models import Team
from users.models import Employee


class AssemblyPartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssemblyPart
        fields = '__all__'
        read_only_fields = ['id', 'installed_at']

class UavsAssemblySerializer(serializers.ModelSerializer):

    class Meta:
        model = UavsAssembly
        fields = '__all__'
        read_only_fields = ['id', 'team', 'assembly_status', 'added_by', 'created_at', 'updated_at']
