# utils.py
from django.utils import timezone
from .models import RecoverPassword
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import serializers
#from ipware import get_client_ip
import socket

# GET CURRENT ADDRESS
def get_system_url(request):
    ip_address = socket.gethostbyname(socket.getfqdn())
    port = request.META.get('SERVER_PORT')
    protocol = 'https' if request.is_secure() else 'http'
    api_path = 'api/v1'

    if port in ['80', '443']:
        system_url = f'{protocol}://{ip_address}/{api_path}'
    else:
        system_url = f'{protocol}://{ip_address}:{port}/{api_path}'

    return system_url


# VALIDADE OTP CODE
def is_valid_otp(user_otp, recover_password):
    if recover_password is None:
        return False
    latest_recover_password = RecoverPassword.objects.filter(user=recover_password.user).order_by('-created_at').first()
    if latest_recover_password is None:
        return False
    if latest_recover_password.otp != user_otp:
        return False
    if latest_recover_password.expiry_datetime < timezone.now():
        return False
    return True

# EXCEPTION_HANDLER
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    # Se houver uma resposta e ela contiver a chave "error" e um array como valor
    if response is not None and isinstance(response.data.get("error"), list):
        # Transforma o array em uma única string
        error_message = ", ".join(response.data["error"])
        # Cria um novo dicionário com a chave "error" e a mensagem de erro como valor
        response.data = {"error": error_message}
        # Define o status code para 400 (Bad Request)
        response.status_code = status.HTTP_400_BAD_REQUEST
    
    return response


# GEO_IP_LOCATION
def get_client_ip(request):
    """
    Retorna o endereço IP do cliente que está fazendo a requisição.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # Em alguns casos, o endereço IP pode ser uma string vazia, retornamos None nesses casos
    if ip == '':
        return None
    # Em alguns casos, o endereço IP pode ser um endereço IPv6, precisamos formatá-lo corretamente
    if ':' in ip:
        ip = socket.inet_ntop(socket.AF_INET6, socket.inet_pton(socket.AF_INET6, ip))
    return ip

