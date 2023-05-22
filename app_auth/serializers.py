from rest_framework import serializers
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import RecoverPassword

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.conf import settings
from django.urls import reverse
import logging
import string
import random
import uuid
import pytz
from datetime import timedelta, datetime
from django.utils import timezone
from .utils import get_system_url, is_valid_otp
from .emails import send_otp_email
from .utils import get_system_url

logger = logging.getLogger(__name__)


# IP BLACK LIST


# RESET PASSWORD 
class ResetPasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("As senhas não são iguais.", code='invalid')
        
        # valida o token fornecido com a base de dados
        token = self.context.get('token')
        try:
            recover_password = RecoverPassword.objects.get(token=token)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("O token fornecido é inválido.", code='invalid')

        expiry_datetime = timezone.localtime(recover_password.expiry_datetime, timezone.get_default_timezone())
        current_datetime = timezone.localtime(timezone.now(), timezone.get_default_timezone())
        remaining_time = expiry_datetime - current_datetime
        if remaining_time.total_seconds() <= 0:
            raise serializers.ValidationError("O token fornecido expirou.", code='invalid')

        if recover_password.is_used:
            raise serializers.ValidationError("O link de recuperação da senha já foi utilizado.", code='invalid')

        self.context['recover_password'] = recover_password

        return data

    def create(self, validated_data):
        # recupera o objeto recover_password do contexto
        recover_password = self.context.get('recover_password')

        user = recover_password.user

        user_from_db = User.objects.filter(email=user.email).first()
        if user_from_db != user:
            raise serializers.ValidationError("O usuário fornecido é inválido.", code='invalid')

        if recover_password.is_used:
            raise serializers.ValidationError("O link de recuperação da senha já foi utilizado.", code='invalid')
        user.set_password(validated_data['password'])
        user.save()

        recover_password.is_used = True
        recover_password.save()

        return {"message": "Senha redefinida com sucesso."}


# OTP CODE VERIFY
class OtpCodeVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, value):
        try:
            recovery_password = RecoverPassword.objects.get(otp=value)
        except RecoverPassword.DoesNotExist:
            raise serializers.ValidationError("Código OTP inválido.")
        self.context['recovery_password'] = recovery_password
        return value

    def validate_expiry_datetime(self, value):
        recovery_password = self.context.get('recovery_password')
        current_datetime = timezone.localtime(timezone.now(), timezone.get_default_timezone())
        if recovery_password.expiry_datetime < current_datetime:
            raise serializers.ValidationError("O código OTP expirou.")
        return value

    def create(self, validated_data):
        recovery_password = self.context.get('recovery_password')
        expiry_datetime = timezone.localtime(recovery_password.expiry_datetime, timezone.get_default_timezone())
        current_datetime = timezone.localtime(timezone.now(), timezone.get_default_timezone())
        remaining_time = expiry_datetime - current_datetime
        user_id = recovery_password.user.id
        token = recovery_password.token
        uidb64 = urlsafe_base64_encode(force_bytes(user_id))
        reset_link = f"{get_system_url(self.context.get('request'))}/reset-password/{uidb64}/{token}/"
        logger.info(f"Hora Registro: {current_datetime}")
        logger.info(f"Hora Expiracao: {expiry_datetime}")
        logger.info(f"Tempo Restante: {remaining_time}")
        
        if remaining_time.total_seconds() <= 0:
            return {"error": "O código OTP expirou."}
        
        return {"url": reset_link}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context['request'] = self.context.get('view').request if self.context.get('view') else None



# RECOVERY PASSWORD
class SendOTPCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        users = User.objects.filter(email=value)
        if not users.exists():
            raise serializers.ValidationError("O endereço de e-mail não está registrado.")
        elif users.count() > 1:
            raise serializers.ValidationError("Existem vários usuários com o mesmo endereço de e-mail.")
        return value


    def create(self, validated_data):
        # Gera o código de 6 dígitos aleatório
        code = ''.join(random.choices('0123456789', k=6))

        # Define a hora de expiração com o timezone padrão
        expiry_datetime = timezone.localtime(timezone.now() + timezone.timedelta(hours=1), timezone.get_default_timezone())

        expiry_datetime_str = expiry_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # Salva as informações em um novo objeto RecoverPassword com o timezone padrão
        recovery_password = RecoverPassword.objects.create(
            user=User.objects.get(email=validated_data['email']),
            otp=code,
            token=str(uuid.uuid4()),
            encoded_token='',
            expiry_datetime=expiry_datetime_str,
            is_used=False,
            reset_link='',
        )

        # Mensagem de log informando o fuso horário padrão
        timezone_name = settings.TIME_ZONE
        timezone_message = f"Usando o fuso horário padrão '{timezone_name}' definido em settings.py."
        logger.info(timezone_message)
        logger.info(expiry_datetime)

        # Envia o e-mail com o código OTP
        send_otp_email(validated_data['email'], code)

        # Retorna o código na resposta
        return {'code': code}


# CREATE USER
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError('As senhas não coincidem.')

        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Nome de usuário já está em uso.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Endereço de email já está em uso.')

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



