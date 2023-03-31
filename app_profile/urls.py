from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserAndProfileViewSet

router = DefaultRouter()
router.register(r'profile', UserAndProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
