import socket
from urllib.parse import urlparse

from django.conf import settings

def get_api_url():
    # Obtém o nome do host
    hostname = socket.gethostname()

    # Obtém o endereço IP do host
    ip_address = socket.gethostbyname(hostname)

    # Obtém a URL base da API a partir das configurações
    API_BASE_URL = settings.API_BASE_URL

    # Analisa a URL da API
    parsed_url = urlparse(API_BASE_URL)

    # Verifica se a porta está presente na URL
    if parsed_url.port:
        # Define a URL da API com a porta
        API_URL = f"http://{ip_address}:{parsed_url.port}{parsed_url.path}"
    else:
        # Define a URL da API sem a porta
        API_URL = f"http://{ip_address}{parsed_url.path}"
    
    return API_URL
