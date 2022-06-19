from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
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
