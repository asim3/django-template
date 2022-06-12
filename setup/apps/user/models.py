from django.utils.translation import gettext_lazy as _
from django.db.models import(
    Model, CharField, DateTimeField, BooleanField, OneToOneField, CASCADE)
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    phone = CharField(
        _("phone"),
        max_length=15,
        null=True,
        blank=True,
        unique=True,
        db_index=True)


class OneTimePassword(Model):
    phone = CharField(_("phone"), max_length=15, unique=True, db_index=True)
    key = CharField(
        _("key"), max_length=settings.OTP_MAX_LENGTH, unique=True, db_index=True)
    created_on = DateTimeField(_("created on"), auto_now_add=True)
    is_verified = BooleanField(_("is verified"), default=False)

    def is_expired(self):
        if self.created_on and self.created_on < timezone.now():
            return False
        return True
