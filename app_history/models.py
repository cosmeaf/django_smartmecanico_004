import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from app_schedule.models import Schedule
from app_employees.models import Employee


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('history_images', filename)

def get_video_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('history_videos', filename)


class ScheduledService(Base):
    STATUS_CHOICES = [
        ('', '----------------'),
        ('pending', 'Pendente'),
        ('started', 'Iniciado'),
        ('ongoing', 'Em andamento'),
        ('finished', 'Finalizado')
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='services')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='services')
    service_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    service_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    service_video = models.FileField(upload_to=get_video_path, null=True, blank=True)
    service_observation = models.TextField(null=True, blank=True)
    vehicle_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    service_time = models.DurationField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    protocol = models.CharField(max_length=50, unique=True)
    additional_info = models.TextField(null=True, blank=True)
    problem_found = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Histórico de Agendamento'
        verbose_name_plural = 'Histórico de Agendamentos'

    def save(self, *args, **kwargs):
        if self.service_status == 'pending':
            self.end_time = None
        if not self.protocol:
            self.protocol = self.schedule.protocol
        super(ScheduledService, self).save(*args, **kwargs)

    def __str__(self):
        return f'Serviço agendado em {self.schedule.day} para o usuário {self.schedule.user} com status {self.service_status}'
