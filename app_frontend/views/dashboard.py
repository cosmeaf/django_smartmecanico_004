import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework_simplejwt.tokens import RefreshToken
from app_profile.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obter o perfil do usuário atual
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            profile = None

        # Gerar token de autenticação
        refresh = RefreshToken.for_user(self.request.user)
        access_token = str(refresh.access_token)

        # Configurar cabeçalhos da solicitação HTTP com o token de autenticação
        headers = {'Authorization': f'Bearer {access_token}'}

        # Fazer solicitação GET para o perfil da API
        profile_url = 'http://10.0.0.10/api/v1/profile/'
        response = requests.get(profile_url, headers=headers)

        # Testar se a resposta da API é bem-sucedida
        if response.status_code == 200:
            profile_data = response.json()[0] # extrair o primeiro (e único) dicionário da lista
            context['profile'] = profile_data
        else:
            return HttpResponseServerError('Erro ao obter os dados do perfil.')

        return context




class DashboardProfileView(TemplateView):
    template_name = 'dashboard/profile.html'