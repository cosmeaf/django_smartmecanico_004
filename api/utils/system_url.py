import socket
import ipaddress
from django.urls import URLPattern
from django.conf import settings

class SystemUrl:
    def __init__(self, request, urlpatterns):
        self.request = request
        self.urlpatterns = urlpatterns

    def get_url_prefix(self):
        for pattern in self.urlpatterns:
            if isinstance(pattern, URLPattern):
                url_prefix = pattern.pattern.regex.pattern.strip('^$')
                return url_prefix
        return ""

    def is_ip_or_domain(self, value):
        try:
            ipaddress.ip_address(value)
            return 'IP'
        except ValueError:
            pass

        try:
            socket.getaddrinfo(value, None)
            return 'Domain'
        except socket.gaierror:
            pass

        return 'Unknown'

    def get_system_url(self):
        current_host = self.request.get_host().split(':')[0]
        server_port = self.request.META['SERVER_PORT']
        host_type = self.is_ip_or_domain(current_host)
        url_prefix = self.get_url_prefix()

        return {
            'host_type': host_type,
            'url_prefix': url_prefix,
            'server_port': server_port,
        }
