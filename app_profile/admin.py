from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .models import Profile

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser', 'profile_image')
    list_select_related = ('profile',)
    readonly_fields = ('date_joined', 'last_login', 'profile_image')
    ordering = ('-date_joined',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def profile_image(self, obj):
        if obj.profile.image:
            return mark_safe('<img src="%s" style="max-width:50px;max-height:50px;" />' % obj.profile.image.url)
        else:
            return '(Sem imagem)'
    profile_image.short_description = 'Imagem'

    def save_model(self, request, obj, form, change):
        if 'profile' in form.changed_data:
            profile = form.cleaned_data['profile']
            profile.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.profile.image:
            obj.profile.image.delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.profile.image:
                obj.profile.image.delete()
        super().delete_queryset(request, queryset)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
