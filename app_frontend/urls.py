from django.urls import path
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from .views.frontend import LoginView, RegisterView, RecoveryView, HomeView, logout_view
from .views.dashboard import DashboardView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('recovery/', RecoveryView.as_view(), name='recovery'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', logout_view, name='logout'),
]
