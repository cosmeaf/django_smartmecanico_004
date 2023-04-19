from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from app_frontend.api_client.api_config import APIClient
from app_frontend.api_client.utils import get_api_url
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

API_URL = get_api_url()
SECRET_KEY = settings.SECRET_KEY


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        api_client = APIClient()
        response = api_client.post(API_URL + '/token/', json={'username': username, 'password': password})

        if response.status_code == 200:
            token = response.json().get('access')
            request.session['token'] = token
            return redirect('dashboard')
        else:
            messages.error(request, 'Não foi possível efetuar login. Verifique suas credenciais.')

        return render(request, self.template_name)


class RegisterView(TemplateView):
    template_name = "register.html"

class RecoveryView(TemplateView):
    template_name = "recovery.html"

from django.shortcuts import redirect

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
