from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
)


class BaseTestCase(TestCase):
    methods_not_allowed = None

    def get_headers(self):
        return {"Content_Type": "application/json"}

    def test_method_not_allowed(self):
        if self.methods_not_allowed:
            for method in self.methods_not_allowed:
                response = getattr(self.client, method)(
                    self.url, **self.get_headers())
                self.assertEqual(response.status_code,
                                 HTTP_405_METHOD_NOT_ALLOWED)

    def add_new_user(self, data):
        user = User.objects.create(username=data['username'])
        if data.get('password'):
            user.set_password(data['password'])
            user.save()
        return user

    def get_user(self, username):
        user, _ = User.objects.get_or_create(username=username)
        return user

    def get_user_token(self, username):
        user = self.get_user(username)
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get_user_refresh_token(self, username):
        refresh = self.get_user_token(username)
        refresh.pop("access")
        return refresh

    def get_user_access_token(self, username):
        refresh = self.get_user_token(username)
        refresh.pop("refresh")
        return refresh


class LoginTest(BaseTestCase):
    """
    Test login
    """
    url = reverse_lazy("v1-login")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']

    def get_headers(self):
        return {
            "Content_Type": "application/json",
            "HTTP_AUTHORIZATION": "Token %s" % self.get_user_token("testlogout"),
        }

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


class RefreshTest(BaseTestCase):
    """
    Test refresh
    """
    url = reverse_lazy("v1-refresh")
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


class RegisterTest(BaseTestCase):
    """
    Test register
    """
    url = reverse_lazy("v1-register")
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
