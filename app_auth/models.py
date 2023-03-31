from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings
import uuid
import pytz
import datetime

User = get_user_model()

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'

    def save(self, *args, **kwargs):
        now = timezone.localtime(timezone.now(), timezone.get_default_timezone())
        if not self.created_at:
            self.created_at = now

        # Remove os microssegundos da data/hora antes de salvar no banco de dados
        self.created_at = self.created_at.replace(microsecond=0)

        super().save(*args, **kwargs)


class RecoverPassword(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    encoded_token = models.TextField()
    expiry_datetime = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    reset_link = models.TextField()

    class Meta:
        verbose_name_plural = 'Recupera Senhas'

    def __str__(self):
        return self.user.email

    def is_token_used(self):
        return self.is_used
