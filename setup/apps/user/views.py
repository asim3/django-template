from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
)

from .models import OneTimePassword, Profile
from .serializers import (
    RegisterSerializer,
    UserInfoSerializer,
    CreateOneTimePasswordSerializer,
    ValidateOneTimePasswordSerializer,
)


class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class CreateOneTimePasswordView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateOneTimePasswordSerializer


class ValidateOneTimePasswordView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateOneTimePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.is_otp_token_valid(serializer.validated_data):
            return self.data_valid(serializer.validated_data)
        return self.data_invalid()

    def is_otp_token_valid(self, validated_data):
        phone = validated_data.get("phone")
        otp_token = validated_data.get("token")
        try:
            otp = OneTimePassword.objects.get(phone=phone, key=otp_token)
            if otp.is_datetime_valid():
                otp.delete()
                return True
        except OneTimePassword.DoesNotExist:
            return False

    def data_invalid(self):
        error_data = {
            "phone": _("The phone or token you entered are not correct"),
            "token": _("The phone or token you entered are not correct"),
        }
        return Response(error_data, status=HTTP_400_BAD_REQUEST)

    def data_valid(self, validated_data):
        phone = validated_data.get("phone")
        user = Profile.objects.get(phone=phone).user
        token_refresh = RefreshToken.for_user(user)
        access_data = {
            "refresh": str(token_refresh),
            "access": str(token_refresh.access_token),
        }
        return Response(access_data, status=HTTP_200_OK)
