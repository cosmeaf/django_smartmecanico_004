from django.contrib import admin
from django import forms
from .models import ScheduledService
from django.utils.html import format_html
from .models import ScheduledService


class ScheduledServiceAdminForm(forms.ModelForm):
    class Meta:
        model = ScheduledService
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScheduledServiceAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['service_image'].widget.attrs['readonly'] = True
            self.fields['service_video'].widget.attrs['readonly'] = True
            if not self.instance.employee.user.is_superuser:
                self.fields['schedule'].widget.attrs['readonly'] = True
                self.fields['employee'].widget.attrs['readonly'] = True
                self.fields['service_status'].widget.attrs['readonly'] = True
                self.fields['vehicle_status'].widget.attrs['readonly'] = True

class ScheduledServiceAdmin(admin.ModelAdmin):
    form = ScheduledServiceAdminForm
    list_display = ('id', 'schedule', 'employee', 'service_status', 'vehicle_status', 'service_image_display', 'service_video_display')
    list_filter = ('schedule', 'employee', 'service_status', 'vehicle_status')
    search_fields = ('schedule__user__username', 'employee__user__username')
    date_hierarchy = 'created_at'

    def service_image_display(self, obj):
        if obj.service_image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.service_image.url))
        else:
            return ''

    service_image_display.short_description = 'Imagem do Serviço'

    def service_video_display(self, obj):
        if obj.service_video:
            return format_html('<video width="320" height="240" controls><source src="{}" type="video/mp4"></video>'.format(obj.service_video.url))
        else:
            return ''

    service_video_display.short_description = 'Vídeo do Serviço'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ScheduledServiceAdmin, self).get_readonly_fields(request, obj)
        if obj and not obj.employee.user.is_superuser:
            readonly_fields += ('schedule', 'employee', 'service_status', 'vehicle_status', 'service_image', 'service_video')
        return readonly_fields

    def get_queryset(self, request):
        qs = super(ScheduledServiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(employee__user=request.user)

admin.site.register(ScheduledService, ScheduledServiceAdmin)
