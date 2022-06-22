from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer, CharField, ValidationError, ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from utilities.utils import (
    clean_phone_number,
    clean_arabic_digits,
    generate_OTP_key,
    send_sms_message,
    SMS_Error,
)

from .models import Profile, OneTimePassword
from .forms import RegistrationForm


class RegisterSerializer(Serializer):
    username = CharField(max_length=150, write_only=True, required=True)
    password = CharField(write_only=True, required=True)
    refresh = CharField(read_only=True)
    access = CharField(read_only=True)
    captcha_key = CharField(write_only=True, required=True)
    captcha_token = CharField(write_only=True, required=True)

    def get_form(self, data):
        return RegistrationForm(data={
            "username": data["username"],
            "password1": data["password"],
            "password2": data["password"],
            "captcha_0": data["captcha_key"],
            "captcha_1": data["captcha_token"],
        })

    def validate(self, data):
        form = self.get_form(data)
        if form.is_valid():
            return data

        if form.errors.get("password2"):
            form.errors["password"] = form.errors.pop("password2")
        raise ValidationError(form.errors)

    def create(self, validated_data):
        form = self.get_form(validated_data)
        if form.is_valid():
            user = form.save()
            token_refresh = RefreshToken.for_user(user)
            return {
                "username": user.username,
                "password": "password",
                "refresh": str(token_refresh),
                "access": str(token_refresh.access_token),
            }
        raise ValidationError(form.errors)


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff', ]
        depth = 1


class CreateOneTimePasswordSerializer(Serializer):
    phone = CharField(max_length=15, required=True)

    def validate_phone(self, value):
        phone = clean_phone_number(value)
        if not phone.isdigit():
            raise ValidationError(_("This is not a valid phone"))
        try:
            User.objects.get(profile__phone=phone)
        except User.DoesNotExist:
            raise ValidationError(
                _("This phone number is not registered"))
        return phone

    def validate(self, attrs):
        phone = attrs.get("phone")
        try:
            instance = OneTimePassword.objects.get(phone=phone)
            if instance.is_datetime_valid():
                raise ValidationError(
                    _("You can request a new OTP after 60 seconds"))
            self.instance = instance
        except OneTimePassword.DoesNotExist:
            pass
        return attrs

    def create(self, validated_data):
        key = generate_OTP_key()
        phone = validated_data["phone"]
        self.send_sms_message(phone, key)
        instance = OneTimePassword.objects.create(phone=phone, key=key)
        return instance

    def update(self, instance, validated_data):
        key = generate_OTP_key()
        self.send_sms_message(instance.phone, key)
        instance.key = key
        instance.created_on = timezone.now()
        instance.save()
        return instance

    def send_sms_message(self, phone, key):
        try:
            text = _("Your OTP is: ") + key
            send_sms_message(phone, text)
        except SMS_Error as errors:
            raise ValidationError({"errors": [str(errors)]})


class ValidateOneTimePasswordSerializer(Serializer):
    phone = CharField(max_length=15, write_only=True, required=True)
    token = CharField(max_length=settings.OTP_MAX_LENGTH,
                      write_only=True, required=True)
    refresh = CharField(read_only=True)
    access = CharField(read_only=True)

    def validate_phone(self, value):
        phone = clean_phone_number(value)
        if not phone.isdigit():
            raise ValidationError(_("This is not a valid phone"))
        return phone

    def validate_token(self, value):
        otp_token = clean_arabic_digits(value)
        if not otp_token.isdigit():
            raise ValidationError(_("This is not a valid token"))
        return otp_token

    def validate(self, attrs):
        phone = attrs.get("phone")
        otp_token = attrs.get("token")
        try:
            otp = OneTimePassword.objects.get(phone=phone, key=otp_token)
            if otp.is_datetime_valid():
                otp.delete()
                return attrs
        except OneTimePassword.DoesNotExist:
            raise ValidationError(
                _("The phone or token you entered are not correct"))
        raise ValidationError(
            _("The phone or token you entered are not correct"))

    def create(self, validated_data):
        phone = validated_data.get("phone")
        user = Profile.objects.get(phone=phone).user
        token_refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(token_refresh),
            "access": str(token_refresh.access_token),
        }
