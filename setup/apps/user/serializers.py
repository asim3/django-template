from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer, CharField, ValidationError, ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from backends.utils import generate_OTP_key, clean_arabic_digits, send_sms_message

from .models import OneTimePassword


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


class OneTimePasswordSerializer(ModelSerializer):

    class Meta:
        model = OneTimePassword
        fields = ["phone"]
        depth = 1

    def validate_phone(self, value):
        phone = clean_arabic_digits(value)
        if not phone.isdigit():
            raise ValidationError(_("This is not a valid phone"))
        if phone.startswith("+"):
            phone = phone[1:]
        if phone.startswith("00"):
            phone = phone[2:]
        if phone.startswith("05"):
            phone = "966" + phone[:-9]
        if phone.startswith("5"):
            phone = "966" + phone[:-9]
        return phone

    def validate(self, data):
        phone = data.get('phone')
        try:
            User.objects.get(profile__phone=phone)
        except User.DoesNotExist:
            raise ValidationError(
                _("This phone number is not registered"))
        return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.key = generate_OTP_key()
        instance.save()
        send_sms_message("Your OTP is: " + instance.key)
        return instance
