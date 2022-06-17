from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


class RegistrationForm(UserCreationForm):
    captcha = CaptchaField(
        label=_("Type the code seen in the image"))
