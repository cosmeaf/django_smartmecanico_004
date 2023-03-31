from rest_framework import serializers
from app_schedule.models import Schedule
from app_employees.models import Employee
from .models import ScheduledService


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'user']


class ScheduledServiceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    service_status = serializers.CharField(source='get_service_status_display')
    vehicle_status = serializers.CharField(source='get_vehicle_status_display')

    class Meta:
        model = ScheduledService
        exclude = ['created_at', 'updated_at', 'deleted_at', 'schedule']

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'employee': instance.employee.user.username,
            'service_status': instance.get_service_status_display(),
            'service_image': instance.service_image.url if instance.service_image else None,
            'service_video': instance.service_video.url if instance.service_video else None,
            'service_observation': instance.service_observation,
            'vehicle_status': instance.get_vehicle_status_display(),
            'start_time': instance.start_time,
            'end_time': instance.end_time,
        }


class ScheduledServiceDetailSerializer(serializers.ModelSerializer):
    schedule = serializers.StringRelatedField()
    employee = EmployeeSerializer()
    service_status = serializers.CharField(source='get_service_status_display')
    vehicle_status = serializers.CharField(source='get_vehicle_status_display')

    class Meta:
        model = ScheduledService
        exclude = ['created_at', 'updated_at', 'deleted_at']

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'schedule': str(instance.schedule),
            'employee': instance.employee.user.username,
            'service_status': instance.get_service_status_display(),
            'service_image': instance.service_image.url if instance.service_image else None,
            'service_video': instance.service_video.url if instance.service_video else None,
            'service_observation': instance.service_observation,
            'vehicle_status': instance.get_vehicle_status_display(),
            'start_time': instance.start_time,
            'end_time': instance.end_time,
        }
