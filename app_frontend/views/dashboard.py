from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from app_frontend.api_client.api_config import APIClient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

API_URL = settings.API_BASE_URL
LOGIN_URL = settings.LOGIN_URL
SECRET_KEY = settings.SECRET_KEY


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        token = request.session.get('token')
        if not token:
            return redirect('login')

        api_client = APIClient(token)
        is_valid = api_client.validate_token(SECRET_KEY)
        if not is_valid:
            messages.error(request, 'Token inválido ou expirado.')
            return redirect('login')

        response = api_client.get(API_URL + '/profile/')
        if response.status_code == 200:
            profile_data = response.json()[0]
            context = {
                'profile': profile_data
            }
        else:
            messages.error(request, 'Não foi possível carregar os dados do perfil.')
            context = {}

        return render(request, self.template_name, context)


class DashboardProfileView(TemplateView):
    template_name = 'dashboard/profile.html'