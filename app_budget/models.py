from django.db import models
from django.contrib.auth.models import User
import uuid

class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=False, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'

class Expense(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_balance()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_balance()

    @property
    def income(self):
        return max(self.amount, 0)

    @property
    def expense(self):
        return min(self.amount, 0)

    @staticmethod
    def get_balance(user):
        expenses = Expense.objects.filter(user=user)
        balance = sum([expense.amount for expense in expenses])
        return balance

    def update_balance(self):
        user = self.user
        balance = Expense.get_balance(user)
        user.profile.balance = balance
        user.profile.save()

    class Meta:
        verbose_name = 'Controle de Gastos'
        verbose_name_plural = 'Controle de Gastos'

    def __str__(self):
        return f"{self.name} ({self.amount})"
