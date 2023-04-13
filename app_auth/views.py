from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse

def api_status(request):
    return JsonResponse({'message': 'API Online'})
    
# RESET PASSWORD VIEW
class ResetPasswordConfirmView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordConfirmSerializer

    def get_serializer_context(self):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        return {'uidb64': uidb64, 'token': token}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response({'message': response_data['message']})

# OTP VERIFY VIEW
class OtpCodeVerifyView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OtpCodeVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data, status=status.HTTP_200_OK)

# REVOCERY PASSWORD VIEW
class SendOTPCodeView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendOTPCodeSerializer
    throttle_scope = 'blocked_ips'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data, status=status.HTTP_200_OK)

# USER CREATE VIEW
class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

