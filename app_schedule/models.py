from django.db import models
from django.contrib.auth.models import User
from app_address.models import Address
from app_vehicles.models import Vehicle
from app_services.models import Service
from app_employees.models import Employee
from datetime import datetime
import uuid



def generate_protocol():
    current_date = datetime.now()
    date_str = current_date.strftime("%d%m%Y")
    uuid_str = str(uuid.uuid4())[:12].upper()
    return f'{date_str}-{uuid_str}'


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True)
    deleted_at = models.DateTimeField('Data de Exclusão', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'

class Schedule(Base):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name='Endereço', on_delete=models.CASCADE, related_name='schedules', related_query_name="schedule")
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.CASCADE, related_name='schedules', related_query_name="schedule")
    service = models.ForeignKey(Service, verbose_name='Serviço', on_delete=models.CASCADE, related_name='schedules', related_query_name="schedule")
    hour = models.CharField('Hora do Serviço', max_length=5)
    day = models.DateField('Data do Serviço', help_text='Escolha uma data disponível')
    protocol = models.CharField('Protocolo', max_length=21, unique=True, default=generate_protocol)
    employee = models.ForeignKey('app_employees.Employee', verbose_name='Mecânico', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'{self.service}'






