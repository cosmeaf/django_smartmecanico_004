from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
import json
import requests
import logging

logger = logging.getLogger(__name__)

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        # Obter as credenciais do usuário a partir do formulário de login
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Fazer request para a API Django Rest Framework para obter o token JWT
        data = {'username': username, 'password': password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://10.0.0.10/api/v1/token/', data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            token = response.json().get('access')

            # Armazenar o token JWT no localStorage
            request.session['access_token'] = token

            # Redirecionar o usuário para a página de dashboard
            return redirect('dashboard')
        else:
            # Exibir mensagem de erro na página de login caso as credenciais sejam inválidas
            return render(request, self.template_name, {'error': 'Invalid credentials'})


class RegisterView(TemplateView):
    template_name = "register.html"

class RecoveryView(TemplateView):
    template_name = "recovery.html"

def logout_view(request):
    # Limpar os cookies
    response = redirect('login')
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    response.delete_cookie('access_token')
    # Limpar a sessão
    request.session.flush() 
    return response



# Home Page
class HomeView(TemplateView):
    template_name = "index.html"

class SobreView(TemplateView):
    template_name = "about.html"

class ServicosView(TemplateView):
    template_name = "services.html"

class TelemetriaView(TemplateView):
    template_name = "telemetry.html"

class ContactView(TemplateView):
    template_name = "contact.html"
