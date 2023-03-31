from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'plate', 'user')
    list_filter = ('brand', 'model', 'year', 'user')
    search_fields = ('brand', 'model', 'year', 'plate', 'user__username')
    list_display_links = ('plate', 'user',)
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']
    actions = ['change_owner', 'select_all_vehicles']

    def change_owner(self, request, queryset):
        users = User.objects.all()
        return render(request, 'admin/change_owner.html', {'users': users, 'queryset': queryset})
    change_owner.short_description = "Change owner of selected vehicles"

    def select_all_vehicles(self, request, queryset):
        queryset.update(selected=True)
    select_all_vehicles.short_description = "Select all vehicles"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions


admin.site.register(Vehicle, VehicleAdmin)
