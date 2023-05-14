from django.contrib import admin
from django.utils.html import format_html
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'salario', 'data_admissao', 'foto')
    list_filter = ('user', 'cargo', 'data_admissao', 'deleted_at')
    search_fields = ('user__username', 'cargo')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')

    def foto(self, obj):
        if obj.profile.image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px;" />', obj.profile.image.url)
        else:
            return '-'

    foto.short_description = 'Foto'

