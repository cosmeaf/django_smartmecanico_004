# from django.apps import AppConfig


# class AppScheduleConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'app_schedule'
from django.apps import AppConfig

class AppScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_schedule'

    def ready(self):
        import app_schedule.signals
