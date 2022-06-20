from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.core import mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_302_FOUND,
    HTTP_400_BAD_REQUEST,
)


from backends.tokens import EmailVerificationTokenGenerator
from .base import BaseTestCase

import re


class RegistrationTest(BaseTestCase):
    """
    Test Registration
    """
    url = reverse_lazy("user-register")
    methods_not_allowed = ['patch', 'delete', 'trace']

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("username", response.context.get('form').errors)
        self.assertIn("password1", response.context.get('form').errors)
        self.assertIn("password2", response.context.get('form').errors)
        self.assertIn("captcha", response.context.get('form').errors)
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_user(self):
        self.get_user("test@user.com")
        data = {
            "username": "test@user.com",
            "password1": "new_password",
            "password2": "new_password",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("username", response.context.get('form').errors)
        username_error = response.context.get('form').errors["username"][0]
        self.assertEqual(
            username_error, _("A user with that email address already exists"))
        self.assertNotIn("password1", response.context.get('form').errors)
        self.assertNotIn("password2", response.context.get('form').errors)
        self.assertNotIn("captcha", response.context.get('form').errors)
        self.assertEqual(User.objects.count(), 1)

    def test_email_syntax(self):
        self.get_user("user1")
        self.get_user_token("user2")
        data = {
            "username": "test@user",
            "password1": "new_password",
            "password2": "new_password",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("username", response.context.get('form').errors)
        username_error = response.context.get('form').errors["username"][0]
        self.assertEqual(username_error, _('Enter a valid email address.'))
        self.assertNotIn("password1", response.context.get('form').errors)
        self.assertNotIn("password2", response.context.get('form').errors)
        self.assertNotIn("captcha", response.context.get('form').errors)
        self.assertEqual(User.objects.count(), 2)

    def test_not_valid_captcha(self):
        self.get_user("user1")
        data = {
            "username": "test@user.com",
            "password1": "new_password",
            "password2": "new_password",
            "captcha_0": "my-test",
            "captcha_1": "0000",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotIn("username", response.context.get('form').errors)
        self.assertNotIn("password1", response.context.get('form').errors)
        self.assertNotIn("password2", response.context.get('form').errors)
        self.assertIn("captcha", response.context.get('form').errors)
        self.assertEqual(User.objects.count(), 1)

    def test_success_response(self):
        self.get_user("user1@user.com")
        self.get_user_token("user2@user.com")
        data = {
            "username": "test@user.com",
            "password1": "new_password",
            "password2": "new_password",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertEqual(response.url, reverse("user-email-verification"))
        self.assertEqual(User.objects.count(), 3)
        new_user = User.objects.get(username="test@user.com")
        self.assertEqual(new_user.email, "test@user.com")
        self.assertEqual(new_user.profile.phone, None)
        self.assertEqual(new_user.profile.is_email_verified, False)


class RegisterAPITest(BaseTestCase):
    """
    Test register
    """
    url = reverse_lazy("v1-user-register")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json().keys())
        self.assertIn('password', response.json().keys())
        self.assertEqual(User.objects.count(), 0)

    def test_duplicate_user(self):
        self.get_user("testuser")
        data = {"username": "testuser", "password": "new_password"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json().keys())
        self.assertEqual(User.objects.count(), 1)

    def test_success_response(self):
        self.get_user("user1")
        self.get_user_token("user2")
        data = {"username": "testuser", "password": "my_password"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        user = self.get_user("testuser")
        self.assertEqual(RefreshToken(response.json()["refresh"]).get(
            "user_id"), user.id)
        self.assertEqual(AccessToken(response.json()["access"]).get(
            "user_id"), user.id)


class EmailVerificationTest(BaseTestCase):
    """
    Test Email Verification
    """
    url = reverse_lazy("user-email-verification")
    methods_not_allowed = None

    def get_email_verification_url(self):
        user = self.get_user()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token_generator = EmailVerificationTokenGenerator()
        token = token_generator.make_token(user)
        return reverse("password_reset_confirm", kwargs={
            "uidb64": uidb64,
            "token": token
        })

    def test_send_email_verification(self):
        response = self.client.post(reverse("user-register"), data={
            "username": "url@email.com",
            "password1": "new_password",
            "password2": "new_password",
            "captcha_0": "my-test",
            "captcha_1": "PASSED",
        })
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, HTTP_302_FOUND)
        self.assertEqual(len(mail.outbox), 1)
        subject = _("Password reset on") + " testserver"
        self.assertEqual(subject, mail.outbox[0].subject)
        self.assertEqual(
            settings.DEFAULT_FROM_EMAIL, mail.outbox[0].from_email)
        self.assertEqual(['url@email.com'], mail.outbox[0].recipients())
        email_body = mail.outbox[0].body
        urlmatch = re.search(r"https?://[^/]*(/.*reset/\S*)", email_body)
        self.assertIsNotNone(urlmatch, "No URL found in sent email")
        return urlmatch[1]
