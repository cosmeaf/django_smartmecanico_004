from rest_framework import serializers
from app_schedule.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    employee = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        exclude = ['created_at', 'updated_at', 'deleted_at']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user': instance.user.username,
            'address': instance.address.cep,
            'service': instance.service.name,
            'vehicle': instance.vehicle.brand,
            'hour': instance.hour,
            'day': instance.day.strftime('%d/%m/%Y'),
            'protocol': instance.protocol,
            'employee': instance.employee.user.username if instance.employee else None
        }


class ScheduleDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField(source='address.cep')
    service = serializers.StringRelatedField(source='service.name')
    vehicle = serializers.StringRelatedField(source='vehicle.brand')
    employee = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'address', 'service', 'vehicle', 'hour', 'day', 'protocol', 'employee']
