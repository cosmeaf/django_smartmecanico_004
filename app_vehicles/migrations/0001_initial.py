# Generated by Django 3.2.17 on 2023-04-17 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Data de Exclusão')),
                ('brand', models.CharField(max_length=255, verbose_name='Marca Veículo')),
                ('model', models.CharField(max_length=255, verbose_name='Modelo Veículo')),
                ('fuel', models.CharField(max_length=255, verbose_name='Combustível')),
                ('year', models.CharField(max_length=4, verbose_name='Ano Fabricação')),
                ('odometer', models.CharField(max_length=9, verbose_name='Hodômetro')),
                ('plate', models.CharField(max_length=10, unique=True, verbose_name='Placa Veículo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
        ),
    ]
