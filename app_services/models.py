from django.db import models
from django.contrib.auth.models import User
import uuid
import os


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


class Service(Base):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('icon', filename)

    image = models.ImageField('Image', upload_to=get_file_path, height_field=None, width_field=None, max_length=None, null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    name = models.CharField('Titulo', max_length=255, editable=True)
    description = models.TextField('Descrição', editable=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f'{self.name}'

    def delete_old_image(self):
        # Deleta a imagem antiga, caso exista e não seja a imagem padrão
        try:
            old_service = Service.objects.get(pk=self.pk)
            if old_service.image.name != self.image.field.default:
                os.remove(old_service.image.path)
        except Service.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        # Deleta a imagem antiga, caso tenha sido trocada por uma nova
        if self.pk:
            self.delete_old_image()

        super().save(*args, **kwargs)


class HourService(Base):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='hour_service')
    hour = models.CharField('Hora Serviço', max_length=8)

    class Meta:
        verbose_name = 'Hour Service'
        verbose_name_plural = 'Hour Services'

    def __str__(self):
        return f'{self.hour}'