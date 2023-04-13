from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = "login.html"

class RegisterView(TemplateView):
    template_name = "register.html"

class RecoveryView(TemplateView):
    template_name = "recovery.html"

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