import logging
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from datetime import datetime
from app_employees.models import Employee


logger = logging.getLogger(__name__)


def send_email_notification(schedule):
    date = schedule.day
    try:
        subject = 'Nova notificação de agendamento'
        message = f'Olá {schedule.user.first_name}, acabamos de registrar seu agendamento para o serviço de {schedule.service.name}.\n Confira abaixo os detalhes:\n\nProtocolo: {schedule.protocol}\nVeículo: {schedule.vehicle.brand} {schedule.vehicle.model}\nEndereço: {schedule.address.logradouro}, {schedule.address.bairro}, {schedule.address.localidade} - {schedule.address.uf}\nData: {schedule.day.strftime("%d/%m/%Y")}\nHorário: {schedule.hour}\n\nObrigado por utilizar nossa plataforma!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [schedule.user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        logger.error(f"Error sending email notification to user {schedule.user.email}: {e}")

def send_sms_notification(schedule):
    date = schedule.day
    try:
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        body = f'Olá {schedule.user.first_name}, acabamos de registrar seu agendamento para o serviço de {schedule.service.name}. Confira abaixo os detalhes:\n\nProtocolo: {schedule.protocol}\nVeículo: {schedule.vehicle.brand} {schedule.vehicle.model}\nEndereço: {schedule.address.logradouro}, {schedule.address.bairro}, {schedule.address.localidade} - {schedule.address.uf}\nData: {schedule.day.strftime("%d/%m/%Y")}\nHorário: {schedule.hour}\n\nObrigado por utilizar nossa plataforma!'
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=schedule.user.profile.phone_number
        )
        print(message.sid)
    except Exception as e:
        logger.error(f"Error sending SMS notification to user {schedule.user.email}: {e}")


def send_email_notification_with_employee(schedule, employee):
    date = schedule.day.strftime('%d/%m/%Y')
    time = schedule.hour
    service = schedule.service.name
    car = f"{schedule.vehicle.brand} {schedule.vehicle.model}"
    address = f"{schedule.address.logradouro}, {schedule.address.bairro}, {schedule.address.localidade} - {schedule.address.uf}"
    first_name = schedule.user.first_name
    last_name = schedule.user.last_name
    email = schedule.user.email

    # Get the employee information
    employee_first_name = employee.user.first_name
    employee_last_name = employee.user.last_name
    employee_image = employee.profile.image.url if employee.profile.image else None

    # Create the message body
    message_body = f"Olá {first_name} {last_name}, acabamos de registrar seu agendamento para o serviço de {service}. \n\nConfira abaixo os detalhes: \n\nProtocolo: {schedule.protocol}\nVeículo: {car}\nEndereço: {address}\nData: {date}\nHorário: {time}\n\nDados do Mecânico:\nNome: {employee_first_name} {employee_last_name}\nImagem: {employee_image}\n\nObrigado por utilizar nossa plataforma!"

    try:
        # Send the e-mail
        send_mail(
            'Nova notificação de agendamento',
            message_body,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

    except Exception as e:
        logger.error(f"Error sending email notification to user {email}: {e}")

