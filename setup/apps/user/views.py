from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .serializers import (
    RegisterSerializer,
    UserInfoSerializer,
    OneTimePasswordSerializer,
)


class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class OneTimePasswordView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OneTimePasswordSerializer
