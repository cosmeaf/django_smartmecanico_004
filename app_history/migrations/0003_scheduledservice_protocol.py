# Generated by Django 3.2.17 on 2023-04-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_history', '0002_alter_scheduledservice_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledservice',
            name='protocol',
            field=models.CharField(blank=True, max_length=21, null=True, verbose_name='Protocolo'),
        ),
    ]