from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
import logging
logger = logging.getLogger(__name__)

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/dashboard/'):
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
            logger.info(f"Token válido para usuário {token}")

            if token:
                try:
                    user, _ = JWTAuthentication().authenticate_credentials(token)
                    request.user = user
                except AuthenticationFailed:
                    pass
            if not request.user.is_authenticated:
                return redirect(reverse_lazy('login'))
        response = self.get_response(request)
        return response

