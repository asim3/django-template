from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer, CharField, ValidationError, ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from backends.utils import (
    clean_phone_number,
    clean_arabic_digits,
    generate_OTP_key,
    send_sms_message,
)

from .models import Profile, OneTimePassword


class RegisterSerializer(Serializer):
    username = CharField(max_length=150, write_only=True, required=True)
    password = CharField(write_only=True, required=True)
    refresh = CharField(read_only=True)
    access = CharField(read_only=True)

    def get_form(self, data):
        return UserCreationForm(data={
            "username": data["username"],
            "password1": data["password"],
            "password2": data["password"]})

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


class CreateOneTimePasswordSerializer(ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = ["phone"]
        depth = 1

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

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.key = generate_OTP_key()
        instance.save()
        send_sms_message(instance.phone, _("Your OTP is: ") + instance.key)
        return instance


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
