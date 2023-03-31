import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


class Profile(Base):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('profile', filename)

    user = models.OneToOneField(User, verbose_name='Usuário', on_delete=models.CASCADE)
    birthday = models.DateField('Aniversário', auto_now=False, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,20}$', message="Numero de telefone deve conter até 14 digitos.")
    phone_number = models.CharField('Contato', validators=[phone_regex], max_length=17, blank=True, null=True)
    image = models.ImageField('Foto', upload_to=get_file_path, height_field=None, width_field=None, max_length=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
