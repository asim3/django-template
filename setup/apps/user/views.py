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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)

from .forms import RegistrationForm, UserPasswordResetForm
from .mixins import SendEmailVerificationMixin, EmailVerificationConfirmMixin
from .serializers import (
    TokenLoginSerializer,
    RefreshAccessSerializer,
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


class TokenLoginAPIView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenLoginSerializer


class TokenRefreshAPIView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = RefreshAccessSerializer


class RegisterAPIView(CreateAPIView):
    """
    Register a new user.

    You should provide a valid CAPTCHA token. To get a CAPTCHA 
    challenge, you can use this endpoint "/v1/captcha/".
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserInfoAPIView(RetrieveAPIView):
    """
    Provide basic information about the current user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class CreateOneTimePasswordAPIView(CreateAPIView):
    """
    Sends an SMS containing a one-time password token to the 
    provided phone number.

    You should provide a valid CAPTCHA token. To get a CAPTCHA 
    challenge, you can use this endpoint "/v1/captcha/".
    """
    permission_classes = [AllowAny]
    serializer_class = CreateOneTimePasswordSerializer


class ValidateOneTimePasswordAPIView(CreateAPIView):
    """
    Takes a one-time password token and returns an access and refresh 
    JSON web token pair to prove the authentication of the token.
    """
    permission_classes = [AllowAny]
    serializer_class = ValidateOneTimePasswordSerializer
