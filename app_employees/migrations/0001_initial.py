# Generated by Django 3.2.17 on 2023-03-30 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_address', '0001_initial'),
        ('app_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Atualização')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('cargo', models.CharField(max_length=100, verbose_name='Cargo')),
                ('salario', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Salário')),
                ('data_admissao', models.DateField(verbose_name='Data de Admissão')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employee', to='app_address.address', verbose_name='Endereço')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='app_profile.profile', verbose_name='Perfil')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
    ]
