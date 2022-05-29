from rest_framework.serializers import Serializer, CharField, ValidationError, ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
