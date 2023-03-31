from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app_history.models import ScheduledService
from app_history.serializers import ScheduledServiceSerializer, ScheduledServiceDetailSerializer


class ScheduledServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledServiceSerializer
    queryset = ScheduledService.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduledServiceDetailSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee)

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = ScheduledService.objects.all()
        else:
            queryset = ScheduledService.objects.filter(employee__user=user)
        return queryset
