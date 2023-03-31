from rest_framework import viewsets
from .serializers import AddressSerializer, AddressDetailSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Address


class AddressViewSet(viewsets.ModelViewSet):
    #authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'create']:
            return AddressSerializer
        elif self.action == 'update':
            return AddressDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
