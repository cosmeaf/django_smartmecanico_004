from django.urls import path
from .views import *

urlpatterns = [
    # Validation Ping Pong
    path('api-status/', api_status),
    path('register/', UserCreateView.as_view(), name='register'),
    path('recovery-password/', SendOTPCodeView.as_view(), name='recovery-password'),
    path('validate-otp/', OtpCodeVerifyView.as_view(), name='validate-otp'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),   
]