# Generated by Django 3.2.17 on 2023-04-18 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_budget', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='owner',
            new_name='user',
        ),
    ]