# Generated by Django 3.2.17 on 2023-04-17 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_employees', '0001_initial'),
        ('app_schedule', '0005_schedule_mechanic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='mechanic',
        ),
        migrations.AddField(
            model_name='schedule',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', related_query_name='schedule', to='app_employees.employee', verbose_name='Mecânico'),
            preserve_default=False,
        ),
    ]