from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets


User = get_user_model()


class UserAndProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(source='profile.birthday', required=False)
    phone_number = serializers.CharField(source='profile.phone_number', required=False)
    image = serializers.ImageField(source='profile.image', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'birthday', 'phone_number', 'image')


class UserAndProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserAndProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
