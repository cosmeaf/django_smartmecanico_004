from django.contrib import admin
from .models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        # Permite que o superusuário edite qualquer despesa
        if request.user.is_superuser:
            return True
        # Permite que o usuário dono da despesa edite sua própria despesa
        if obj is not None and obj.user == request.user:
            return True
        # Impede que qualquer outro usuário edite a despesa
        return False

    def save_model(self, request, obj, form, change):
        # Define o usuário atual como proprietário da despesa (se o usuário não for o superusuário)
        if not request.user.is_superuser:
            obj.user = request.user
        obj.save()

class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount_display', 'created_at', 'user')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    actions = ['change_owner']

    def amount_display(self, obj):
        # Adiciona o prefixo "R$" antes do valor da despesa
        return f"R$ {obj.amount:.2f}"
    amount_display.short_description = 'Amount'

    def change_owner(self, request, queryset):
        users = User.objects.all()
        return render(request, 'admin/change_owner.html', {'users': users, 'queryset': queryset})
    change_owner.short_description = "Change owner of selected expenses"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions
