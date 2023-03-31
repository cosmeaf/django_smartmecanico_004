from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Profile
from .serializers import *

User = get_user_model()


class UserAndProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserAndProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(id=user.id)




# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

#     def get_serializer_class(self):
#         if self.action in ['update', 'partial_update']:
#             return UserAndProfileUpdateSerializer
#         return self.serializer_class

#     def get_permissions(self):
#         if self.action == 'create':
#             return [permissions.AllowAny()]
#         return [permissions.IsAuthenticated()]
