import requests
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from app_frontend.api_client.get_jwt_token import get_authenticated_data
from api.settings import API_BASE_URL, API_VERSION


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        access_token = request.session.get('access_token')
        if not access_token:
            return redirect('login')

        profile_url = f'{API_BASE_URL}/{API_VERSION}/profile/'  # Atualize para a URL correta do endpoint do perfil.
        profile_data = get_authenticated_data(profile_url, access_token)

        if profile_data:
            return render(request, self.template_name, {'profile': profile_data})
        else:
            return render(request, self.template_name, {'error_message': 'Erro ao obter os dados do perfil.'})



class DashboardProfileView(TemplateView):
    template_name = 'dashboard/profile.html'