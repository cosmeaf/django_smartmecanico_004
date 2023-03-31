from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_otp_email(recipient_email, code):
    subject = 'Seu código de verificação'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]
    html_message = render_to_string('emails/otp_email.html', {'code': code})
    send_mail(
        subject,
        message=None,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )