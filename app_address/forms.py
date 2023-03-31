from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cep'].widget.attrs.update({'class': 'form-control', 'placeholder': 'CEP'})
        self.fields['logradouro'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Logradouro'})
        self.fields['complemento'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Complemento'})
        self.fields['bairro'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Bairro'})
        self.fields['localidade'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Localidade'})
        self.fields['uf'].widget.attrs.update({'class': 'form-control', 'placeholder': 'UF'})
