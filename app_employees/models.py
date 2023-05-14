from django.db import models
from django.contrib.auth.models import User
from app_address.models import Address
from app_profile.models import Profile
import uuid


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Última Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'


class Employee(Base):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('icon', filename)
        
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE, related_name='employees', related_query_name='employee')
    address = models.ForeignKey(Address, verbose_name='Endereço', on_delete=models.CASCADE, related_name='employees', related_query_name='employee')
    profile = models.OneToOneField(Profile, verbose_name='Perfil', on_delete=models.CASCADE, related_name='employee')
    cargo = models.CharField('Cargo', max_length=100)
    salario = models.DecimalField('Salário', max_digits=8, decimal_places=2)
    data_admissao = models.DateField('Data de Admissão', auto_now=False, auto_now_add=False)
 
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.user.username


class EmployeeRating(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'employee')