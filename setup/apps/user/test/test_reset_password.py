from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_302_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from .base import BaseTestCase


class UserPasswordResetTest(BaseTestCase):
    """
    Test User Password Reset
    """
    url = reverse_lazy("admin_password_reset")
    methods_not_allowed = ['patch', 'delete', 'trace']


class UserPasswordResetDoneTest(BaseTestCase):
    """
    Test User Password Reset Done
    """
    url = reverse_lazy("password_reset_done")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']


class UserPasswordResetConfirmTest(BaseTestCase):
    """
    Test User Password Reset Confirm
    """
    url = reverse_lazy(
        "password_reset_confirm",
        kwargs={"uidb64": "eee", "token": "eee"}
    )
    methods_not_allowed = None


class UserPasswordResetCompleteTest(BaseTestCase):
    """
    Test User Password Reset Complete
    """
    url = reverse_lazy("password_reset_complete")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']
