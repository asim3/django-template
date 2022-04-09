from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer


class LogoutAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Token.objects.get(user=self.request.user)


class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
