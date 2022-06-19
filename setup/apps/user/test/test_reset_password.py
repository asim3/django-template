from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.core import mail
from django.contrib.auth.models import User
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

    def test_success_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(_('Password reset'), response.context.get('title'))

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("email", response.context.get('form').errors)
        self.assertIn("captcha", response.context.get('form').errors)
        self.assertEqual(User.objects.count(), 0)

    def test_email_does_not_exist(self):
        User.objects.create(email="test1@user.com")
        data = {
            "email": "test2@user.com",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertIn(response.url, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_email_syntax(self):
        data = {"email": "test@user"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("email", response.context.get('form').errors)
        self.assertIn("captcha", response.context.get('form').errors)

    def test_not_valid_captcha(self):
        data = {
            "email": "test@user.com",
            "captcha_0": "my-test",
            "captcha_1": "0000",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotIn("email", response.context.get('form').errors)
        self.assertIn("captcha", response.context.get('form').errors)
        self.assertEqual(len(mail.outbox), 0)

    def test_success_post(self):
        User.objects.create(email="test@user.com")
        data = {
            "email": "test@user.com",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertIn(response.url, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        subject = _("Password reset on") + " testserver"
        self.assertEqual(subject, mail.outbox[0].subject)
        self.assertEqual("info@gmail.com", mail.outbox[0].from_email)
        self.assertEqual(['test@user.com'], mail.outbox[0].recipients())


class UserPasswordResetDoneTest(BaseTestCase):
    """
    Test User Password Reset Done
    """
    url = reverse_lazy("password_reset_done")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']

    def test_success_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(_('Password reset sent'),
                         response.context.get('title'))


class UserPasswordResetConfirmTest(BaseTestCase):
    """
    Test User Password Reset Confirm
    """
    url = reverse_lazy(
        "password_reset_confirm",
        kwargs={"uidb64": "eee", "token": "eee"}
    )
    methods_not_allowed = None

    def test_not_valid_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(_('Password reset unsuccessful'),
                         response.context.get('title'))
        self.assertFalse(response.context.get('validlink'))
        # self.assertEqual(_('Enter new password'),
        #                  response.context.get('title'))


class UserPasswordResetCompleteTest(BaseTestCase):
    """
    Test User Password Reset Complete
    """
    url = reverse_lazy("password_reset_complete")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']

    def test_success_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(_('Password reset complete'),
                         response.context.get('title'))
