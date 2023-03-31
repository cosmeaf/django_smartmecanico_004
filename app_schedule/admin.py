from django.contrib import admin
from django.contrib.admin.actions import delete_selected
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('address', 'vehicle', 'service', 'hour', 'day', 'user')
    ordering = ['created_at']
    search_fields = ['day']
    list_filter = ('user',)
    list_display_links = ('address', 'vehicle', 'service', 'day', 'user')
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(ScheduleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Change Method for save Service data on Database
        """
        if request.user.is_superuser:
            obj.user = form.cleaned_data.get('user')
        else:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to add user field on admin
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['user'].widget = forms.HiddenInput()
        return form
