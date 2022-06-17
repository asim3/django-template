from django.utils.translation import gettext_lazy as _
from django.db.models import(
    Model, CharField, DateTimeField, BooleanField, OneToOneField, CASCADE)
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


OTP_DEFAULT_AGE = timezone.timedelta(seconds=settings.OTP_DEFAULT_AGE)


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    is_email_verified = BooleanField(_('Email Verified'), default=False)
    phone = CharField(
        _("phone"),
        max_length=15,
        null=True,
        blank=True,
        unique=True,
        db_index=True)


class OneTimePassword(Model):
    phone = CharField(_("phone"), max_length=15, unique=True, db_index=True)
    key = CharField(_("key"), max_length=settings.OTP_MAX_LENGTH)
    created_on = DateTimeField(_("created on"), auto_now_add=True)

    def is_datetime_valid(self):
        expired_date = timezone.now() - OTP_DEFAULT_AGE
        if self.created_on and expired_date < self.created_on:
            return True
        self.delete_expired()
        return False

    @classmethod
    def delete_expired(cls):
        expired_date = timezone.now() - OTP_DEFAULT_AGE
        cls.objects.filter(created_on__lt=expired_date).delete()
