import logging
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from app_schedule.models import Schedule
from app_profile.models import Profile
from app_employees.models import Employee
from app_schedule.notifications import send_email_notification, send_sms_notification, send_email_notification_with_employee
from datetime import datetime

logger = logging.getLogger(__name__)
logger.info("Signal registered")

@receiver(post_save, sender=Schedule)
def send_schedule_notification(sender, instance, created, **kwargs):
    if created:
        try:
            user = instance.user
            profile = Profile.objects.get(user=user)
            car = f"{instance.vehicle.brand} {instance.vehicle.model}"
            address = f"{instance.address.logradouro}, {instance.address.bairro}, {instance.address.localidade} - {instance.address.uf}"
            service = instance.service.name
            date = instance.day.strftime('%d/%m/%Y')
            time = instance.hour
            first_name = user.first_name
            last_name = user.last_name
            phone_number = profile.phone_number
            email = user.email

            logger.info(f"Notificação de novo agendamento enviada para {first_name} {last_name} - Carro: {car}, Endereço: {address}, Serviço: {service}, Data: {date}, Hora: {time}, Telefone: {phone_number}, Email: {email}")

            send_email_notification(instance)
            send_sms_notification(instance)

        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")

@receiver(pre_save, sender=Schedule)
def update_schedule(sender, instance, **kwargs):
    try:
        old_schedule = Schedule.objects.get(pk=instance.pk)
    except Schedule.DoesNotExist:
        return  # se a instância antiga não existir, não faz nada
        
    if instance.day != old_schedule.day or instance.hour != old_schedule.hour or instance.service != old_schedule.service or instance.vehicle != old_schedule.vehicle or instance.address != old_schedule.address:
        try:
            user = instance.user
            profile = Profile.objects.get(user=user)
            car = f"{instance.vehicle.brand} {instance.vehicle.model}"
            address = f"{instance.address.logradouro}, {instance.address.bairro}, {instance.address.localidade} - {instance.address.uf}"
            service = instance.service.name
            date = instance.day.strftime('%d/%m/%Y')
            time = instance.hour
            first_name = user.first_name
            last_name = user.last_name
            phone_number = profile.phone_number
            email = user.email

            logger.info(f"Notificação de atualização enviada para {first_name} {last_name} - Carro: {car}, Endereço: {address}, Serviço: {service}, Data: {date}, Hora: {time}, Telefone: {phone_number}, Email: {email}")

            send_email_notification(instance)
            send_sms_notification(instance)

        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")


######################################################################
@receiver(pre_save, sender=Schedule)
def update_employee(sender, instance, **kwargs):
    try:
        old_schedule = Schedule.objects.get(pk=instance.pk)
    except Schedule.DoesNotExist:
        return  # se a instância antiga não existir, não faz nada

    if instance.employee != old_schedule.employee:
        try:
            employee = instance.employee
            user = employee.user
            profile = employee.profile

            # Send notification email with employee data
            send_email_notification_with_employee(instance, employee)
            logger.info(f"Email de notificação enviado para {instance.user.email}")

        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {e}")





