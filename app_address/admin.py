from django.contrib import admin
from django import forms
from .models import Address
from django.contrib.auth.models import User
from django.utils import timezone

class AddressAdminForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select,
    )

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        if not user:
            raise forms.ValidationError('É necessário selecionar um usuário.')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    form = AddressAdminForm
    list_display = ('cep', 'logradouro', 'complemento',
                    'bairro', 'localidade', 'uf', 'created_at', 'updated_at', 'deleted_at', 'user')
    ordering = ['created_at']
    search_fields = ['cep', 'user']
    list_display_links = ('cep',)
    readonly_fields = ['created_at', 'updated_at', 'deleted_at']

    def user(self, instance):
        return f'{instance.user.get_full_name()}'

    def get_queryset(self, request):
        """
        Show result user by id
        """
        queryset = super(AddressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user_id=request.user)

    def save_model(self, request, obj, form, change):
        """
        Change Method for save Address data on Database
        """
        if request.user.is_superuser and form.cleaned_data.get('user'):
            obj.user = form.cleaned_data.get('user')
        super().save_model(request, obj, form, change)

    def search_cep(self, obj):
        if obj.cep:
            url = f'https://viacep.com.br/ws/{obj.cep}/json/'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                obj.logradouro = data.get('logradouro', '')
                obj.complemento = data.get('complemento', '')
                obj.bairro = data.get('bairro', '')
                obj.localidade = data.get('localidade', '')
                obj.uf = data.get('uf', '')
                obj.ibge = data.get('ibge', '')
                obj.gia = data.get('gia', '')
                obj.siafi = data.get('siafi', '')
                obj.save()

    search_cep.short_description = 'Buscar endereço pelo CEP'

    actions_on_top = True
    actions_on_bottom = True

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        self.message_user(request, f'{queryset.count()} endereço(s) marcado(s) como deletado(s).')

    delete_selected.short_description = 'Marcar selecionados como deletados'
