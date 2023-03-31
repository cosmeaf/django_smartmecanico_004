from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Schedule
from .serializers import ScheduleSerializer, ScheduleDetailSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScheduleDetailSerializer
        elif self.action == 'list':
            return ScheduleListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Schedule.objects.all()
        else:
            queryset = Schedule.objects.filter(user=user)

        return queryset
