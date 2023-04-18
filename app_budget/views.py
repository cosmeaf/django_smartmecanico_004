from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer, ExpenseDetailSerializer

class IsExpenseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite apenas que o proprietário da despesa acesse a visualização detalhada ou faça alterações
        return obj.user == request.user

class ExpenseModelViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ExpenseSerializer
        else:
            return ExpenseDetailSerializer

    def get_queryset(self):
        # Retorna apenas as despesas do usuário atual
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Define o usuário atual como proprietário da nova despesa criada
        serializer.save(user=self.request.user)

    def get_permissions(self):
        # Retorna permissões diferentes dependendo da ação executada
        if self.action in ['list', 'create']:
            # Permite que usuários autenticados criem novas despesas e visualizem apenas suas próprias despesas
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Permite que apenas proprietários de despesas atualizem/excluam despesas
            permission_classes = [permissions.IsAuthenticated, IsExpenseOwner]

        return [permission() for permission in permission_classes]
