from rest_framework import viewsets, permissions
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleDetailSerializer


class IsVehicleOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite apenas que o proprietário do veículo acesse a visualização detalhada ou faça alterações
        return obj.user == request.user


class VehicleModelViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def get_queryset(self):
        # Retorna apenas os veículos do usuário atual
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Define o usuário atual como proprietário do novo veículo criado
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Retorna permissões diferentes dependendo da ação executada
        if self.action in ['list', 'create']:
            # Permite que usuários autenticados criem novos veículos e visualizem apenas seus próprios veículos
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Permite que apenas proprietários de veículos atualizem/excluam veículos
            permission_classes = [permissions.IsAuthenticated, IsVehicleOwner]

        return [permission() for permission in permission_classes]
