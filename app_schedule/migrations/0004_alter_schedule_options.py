# Generated by Django 3.2.17 on 2023-04-17 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_schedule', '0003_alter_schedule_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Agendamento', 'verbose_name_plural': 'Agendamentos'},
        ),
    ]