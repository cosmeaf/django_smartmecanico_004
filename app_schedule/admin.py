from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'vehicle', 'service', 'hour', 'day', 'protocol', 'employee')
    ordering = ['created_at']
    search_fields = ['day', 'protocol', 'employee__user__username']
    list_filter = ('user', 'employee')
    list_display_links = ('user', 'address', 'vehicle', 'service', 'day')
    readonly_fields = ['created_at', 'updated_at', 'deleted_at', 'protocol']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.user = form.cleaned_data.get('user')
        else:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].widget = forms.HiddenInput()
        return form
