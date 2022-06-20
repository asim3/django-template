from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, RedirectView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)

from .forms import RegistrationForm, UserPasswordResetForm
from .mixins import SendEmailVerificationMixin, EmailVerificationConfirmMixin
from .serializers import (
    RegisterSerializer,
    UserInfoSerializer,
    CreateOneTimePasswordSerializer,
    ValidateOneTimePasswordSerializer,
)


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'user/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user-email-verification')
    success_message = _("Your profile was created successfully")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class SendEmailVerificationView(
        LoginRequiredMixin,
        SendEmailVerificationMixin,
        RedirectView):
    url = reverse_lazy('home')


class EmailVerificationConfirmView(EmailVerificationConfirmMixin, RedirectView):
    url = reverse_lazy('home')


class UserPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset_form.html'
    email_template_name = 'user/password_reset_email.html'
    subject_template_name = 'user/password_reset_subject.txt'
    form_class = UserPasswordResetForm


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/password_reset_confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user/password_reset_complete.html'


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
