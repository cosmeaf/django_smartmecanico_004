from rest_framework import serializers
from .models import Service, HourService


class HourServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourService
        fields = ['id', 'hour']
        

class ServiceSerializer(serializers.ModelSerializer):
    hour_service = HourServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Service
        fields = ['id', 'image', 'name', 'description', 'hour_service']
