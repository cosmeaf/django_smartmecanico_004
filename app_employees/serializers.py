from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField(source='address.cep')
    profile = serializers.StringRelatedField(source='profile.name')

    class Meta:
        model = Employee
        exclude = ['created_at', 'updated_at', 'deleted_at']

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'user': instance.user.username,
            'address': instance.address.cep,
            'profile': instance.profile.name,
            'cargo': instance.cargo,
            'salario': str(instance.salario),
            'data_admissao': instance.data_admissao.strftime('%d/%m/%Y'),
        }

class EmployeeDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField()
    profile = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'address', 'profile', 'cargo', 'salario', 'data_admissao']
