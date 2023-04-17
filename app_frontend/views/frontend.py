from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from app_frontend.api_client.api_config import ApiConfig
from django.contrib.auth import logout

class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Obtenha o token JWT do projeto Django com simple-jwt.
            api_config = ApiConfig()
            access_token = api_config.get_jwt_token(username, password)

            if access_token:
                request.session['access_token'] = access_token
                login(request, user)
                return redirect('dashboard')
            else:
                # Erro ao obter o token JWT.
                return render(request, self.template_name, {'error_message': 'Erro ao obter o token JWT.'})
        else:
            # Erro na autenticação.
            return render(request, self.template_name, {'error_message': 'Nome de usuário ou senha incorretos.'})



class RegisterView(TemplateView):
    template_name = "register.html"

class RecoveryView(TemplateView):
    template_name = "recovery.html"

def logout_view(request):
    if request.user.is_authenticated:
        if 'access_token' in request.session:
            del request.session['access_token']
        logout(request)
    return redirect('login')

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
