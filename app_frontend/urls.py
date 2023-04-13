from django.urls import path, include
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from .views.frontend import LoginView, RegisterView, RecoveryView, HomeView
from .views.dashboard import DashboardView


dashboard_patterns = [
    path('', TemplateView.as_view(template_name="dashboard/index.html"), name='dashboard-home'),
    # adicione aqui as suas outras views da dashboard
]


urlpatterns = [
    # Authentications Endpoint
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recovery/', RecoveryView.as_view(), name='recovery'),
    path('dashboard/', include((dashboard_patterns, 'dashboard'), namespace='dashboard')),
]


for pattern in dashboard_patterns:
    pattern.callback.authentication_classes = [JWTAuthentication]
    pattern.callback.permission_classes = [IsAuthenticated]