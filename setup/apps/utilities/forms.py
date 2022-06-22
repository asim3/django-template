from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from django.forms import Form


class CaptchaTestForm(Form):
    captcha = CaptchaField()
