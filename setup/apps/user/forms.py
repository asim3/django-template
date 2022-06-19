from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import EmailField
from captcha.fields import CaptchaField
from django.contrib.auth.forms import PasswordResetForm

from .models import Profile


class RegistrationForm(UserCreationForm):
    username = EmailField(
        label=_('Email Address'),
        max_length=150,
        error_messages={
            'unique': _("A user with that email address already exists"),
        }
    )
    captcha = CaptchaField(label=_("Type the code seen in the image"))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        user.save()
        Profile.objects.create(user=user)
        return user


class UserPasswordResetForm(PasswordResetForm):
    captcha = CaptchaField(label=_("Type the code seen in the image"))
