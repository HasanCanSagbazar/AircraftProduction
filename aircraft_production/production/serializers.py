from rest_framework import serializers
from .models import PartProduction

class PartProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartProduction
        fields = '__all__'
        read_only_fields = ['id', 'team', 'status', 'is_deleted', 'added_by', 'created_at', 'updated_at']