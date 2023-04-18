from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Expense
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}

class ExpenseDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Expense
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}
