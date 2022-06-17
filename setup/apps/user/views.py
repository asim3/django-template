from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)

from .forms import RegistrationForm
from .serializers import (
    RegisterSerializer,
    UserInfoSerializer,
    CreateOneTimePasswordSerializer,
    ValidateOneTimePasswordSerializer,
)


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'user/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = _("Your profile was created successfully")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class RegisterAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class CreateOneTimePasswordAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateOneTimePasswordSerializer


class ValidateOneTimePasswordAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ValidateOneTimePasswordSerializer
