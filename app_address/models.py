from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Base(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'

class Address(Base):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='address')
    cep = models.CharField('Cep', max_length=10)
    logradouro = models.CharField('Logradouro', max_length=255, blank=False, null=False)
    complemento = models.CharField('Complemento', max_length=255, blank=False, null=False)
    bairro = models.CharField('Bairro', max_length=255, blank=False, null=False)
    localidade = models.CharField('Cidade', max_length=255, blank=False, null=False)
    uf = models.CharField('Estado', max_length=2,  blank=False, null=False, editable=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.logradouro}, {self.localidade} - {self.uf}'