from django.db import models
from django.contrib.auth.models import User
import uuid


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=False, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


class Vehicle(Base):
    """Model definition for Vehicle."""
    brand = models.CharField('Marca Veículo', max_length=255, blank=False, null=False)
    model = models.CharField('Modelo Veículo', max_length=255, blank=False, null=False)
    fuel = models.CharField('Combustível', max_length=255, blank=False, null=False)
    year = models.CharField('Ano Fabricação', max_length=4, blank=False, null=False)
    odometer = models.CharField('Hodômetro', max_length=9, blank=False, null=False)
    plate = models.CharField('Placa Veículo', max_length=10, blank=False, null=False, unique=True)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='vehicles')

    class Meta:
        """Meta definition for Vehicle."""
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        """Unicode representation of Vehicle."""
        return self.brand
