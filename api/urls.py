from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# IMPORT APPLICATIONS VIEW
from app_address.views import AddressViewSet
from app_profile.views import UserAndProfileViewSet
from app_vehicles.views import VehicleModelViewSet
from app_services.views import ServiceModelViewSet, HourServiceModelViewSet
from app_schedule.views import ScheduleViewSet
from app_history.views import ScheduledServiceViewSet

# ROUTERs
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'address', AddressViewSet)
router.register(r'profile', UserAndProfileViewSet)
router.register(r'vehicle', VehicleModelViewSet)
router.register(r'services', ServiceModelViewSet)
router.register(r'hour-service', HourServiceModelViewSet)
router.register(r'schedule', ScheduleViewSet, basename='schedule')
router.register(r'scheduled-services', ScheduledServiceViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('app_auth.urls')),
    path('api/v1/', include(router.urls)),
    # FrontEnd Web
    path('', include('app_frontend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)