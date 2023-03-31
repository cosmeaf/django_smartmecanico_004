from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Service, HourService
from .serializers import ServiceSerializer, HourServiceSerializer

class ServiceModelViewSet(ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class HourServiceModelViewSet(ReadOnlyModelViewSet):
    queryset = HourService.objects.all()
    serializer_class = HourServiceSerializer