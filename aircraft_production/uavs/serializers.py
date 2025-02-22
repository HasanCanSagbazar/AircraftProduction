from rest_framework import serializers
from .models import Uavs


class UAVSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uavs
        fields = "__all__"
        read_only_fields = ["id", "status", "stock_quantity", "created_at", "updated_at"]


class UAVSStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uavs
        fields = ['status']