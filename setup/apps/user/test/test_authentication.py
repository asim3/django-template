from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
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


class LoginAPITest(BaseTestCase):
    """
    Test login
    """
    url = reverse_lazy("v1-user-login")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json().keys())
        self.assertIn('password', response.json().keys())

    def test_wrong_password(self):
        self.add_new_user({"username": "testuser", "password": "my_password"})
        data = {"username": "testuser", "password": "wrong_password"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json().keys())

    def test_success_response(self):
        data = {"username": "testuser", "password": "my_password"}
        user = self.add_new_user(data)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(RefreshToken(response.json()["refresh"]).get(
            "user_id"), user.id)
        self.assertEqual(AccessToken(response.json()["access"]).get(
            "user_id"), user.id)


class RefreshAPITest(BaseTestCase):
    """
    Test refresh
    """
    url = reverse_lazy("v1-user-refresh")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response.json().keys())

    def test_empty_token(self):
        data = {'refresh': ''}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response.json().keys())

    def test_wrong_token(self):
        data = {'refresh': 'eyJ0eXAiOiJKV1QiLCUzI1NiJ9.eyJ0b2t.lbGlowGuPuH'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.json().keys())
        self.assertIn('code', response.json().keys())

    def test_success_response(self):
        user = self.get_user("testuser")
        data = self.get_user_refresh_token("testuser")
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', response.json().keys())
        access_token = AccessToken(response.json()["access"])
        self.assertEqual(access_token.get("user_id"), user.id)


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


class UserInfoAPITest(BaseTestCase):
    """
    Test user info
    """
    url = reverse_lazy("v1-user-info")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']
    requires_authorization = True

    def test_success_response(self):
        user = self.get_user("success_user")
        headers = {
            "Content_Type": "application/json",
            "HTTP_AUTHORIZATION": self.get_user_bearer_head("success_user"),
        }
        response = self.client.get(self.url, **headers)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["username"], user.username)
        self.assertEqual(response.json()["first_name"], user.first_name)
        self.assertEqual(response.json()["last_name"], user.last_name)
        self.assertEqual(response.json()["email"], user.email)
        self.assertEqual(response.json()["is_staff"], user.is_staff)


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
        self.assertEqual(response.url, reverse("home"))
        self.assertEqual(User.objects.count(), 3)
        new_user = User.objects.get(username="test@user.com")
        self.assertEqual(new_user.email, "test@user.com")
        self.assertEqual(new_user.profile.phone, None)
        self.assertEqual(new_user.profile.is_email_verified, False)
