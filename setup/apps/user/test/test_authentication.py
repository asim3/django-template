from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
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

    def test_customized_access_token(self):
        data = {"username": "testuser", "password": "my_password"}
        user = self.add_new_user(data)
        user.first_name = "test first name"
        user.last_name = "test last name"
        user.email = "email"
        user.save()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', response.json().keys())
        access_token = AccessToken(response.json()["access"])
        self.assertEqual(access_token.payload["user_id"],
                         user.id)
        self.assertEqual(access_token.payload["username"],
                         user.get_username())
        self.assertEqual(access_token.payload["short_name"],
                         user.get_short_name())
        self.assertEqual(access_token.payload["full_name"],
                         user.get_full_name())
        self.assertEqual(access_token.payload["permissions"],
                         user.get_permissions_as_str())

    def test_customized_refresh_token(self):
        data = {"username": "testuser", "password": "my_password"}
        user = self.add_new_user(data)
        user.first_name = "test first name"
        user.last_name = "test last name"
        user.email = "email"
        user.save()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('refresh', response.json().keys())
        refresh_token = RefreshToken(response.json()["refresh"])
        self.assertEqual(refresh_token.payload["user_id"],
                         user.id)
        self.assertEqual(refresh_token.payload["username"],
                         user.get_username())
        self.assertEqual(refresh_token.payload["short_name"],
                         user.get_short_name())
        self.assertEqual(refresh_token.payload["full_name"],
                         user.get_full_name())
        self.assertEqual(refresh_token.payload["permissions"],
                         user.get_permissions_as_str())


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

    def test_customized_access_token(self):
        user = self.get_user("testuser")
        user.first_name = "test first name"
        user.last_name = "test last name"
        user.email = "email"
        user.save()
        data = self.get_user_refresh_token("testuser")
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('access', response.json().keys())
        access_token = AccessToken(response.json()["access"])
        self.assertEqual(access_token.payload["user_id"], user.id)
        self.assertEqual(access_token.payload["username"], user.get_username())
        self.assertEqual(
            access_token.payload["short_name"], user.get_short_name())
        self.assertEqual(
            access_token.payload["full_name"], user.get_full_name())
        self.assertEqual(access_token.payload["permissions"],
                         user.get_permissions_as_str())

    def test_customized_access_token_keys(self):
        data = self.get_user_refresh_token("testuser")
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        access_token = AccessToken(response.json()["access"])
        self.assertIn("user_id", access_token.payload.keys())
        self.assertIn("username", access_token.payload.keys())
        self.assertIn("short_name", access_token.payload.keys())
        self.assertIn("full_name", access_token.payload.keys())
        self.assertIn("permissions", access_token.payload.keys())


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
