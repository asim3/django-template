from rest_framework.serializers import Serializer, CharField, ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import UserCreationForm


class RegisterSerializer(Serializer):
    username = CharField(max_length=150, write_only=True, required=True)
    password = CharField(write_only=True, required=True)
    token = CharField(read_only=True)

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
            token = Token.objects.create(user=user)
            return {
                "username": user.username,
                "password": "password",
                "token": token.key
            }
        raise ValidationError(form.errors)
