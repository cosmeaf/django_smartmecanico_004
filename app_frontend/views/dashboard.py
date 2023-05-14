from django.views.generic import TemplateView
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
import requests
import logging

logger = logging.getLogger(__name__)

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('access_token'):
            return redirect('login')

        token = request.session['access_token']

        # Fazer request para a API Django Rest Framework para obter os dados do perfil
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get('http://10.0.0.10/api/v1/profile/', headers=headers)

        if response.status_code == 200:
            profile_data = response.json()[0]
            logger.info(profile_data)
            return render(request, self.template_name, {'profile': profile_data})
        else:
            # Exibir mensagem de erro na página de dashboard caso ocorra um erro na API
            return render(request, self.template_name, {'error': 'Error retrieving profile data'})



class DashboardProfileView(TemplateView):
    template_name = 'dashboard/profile.html'