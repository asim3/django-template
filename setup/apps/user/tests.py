from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
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

    def add_new_user_with_token(self, data):
        user = self.add_new_user(data)
        token = Token.objects.create(user=user)
        return (user, token.key,)

    def get_user(self, username):
        user, _ = User.objects.get_or_create(username=username)
        return user

    def get_user_token(self, username):
        token, _ = Token.objects.get_or_create(user=self.get_user(username))
        return token.key


class LoginTest(BaseTestCase):
    """
    Test login
    """
    url = reverse_lazy("v1-login")
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
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json().keys())

    def test_success_response(self):
        data = {"username": "testuser", "password": "my_password"}
        user, token = self.add_new_user_with_token(data)
        response = self.client.post(self.url, data=data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected = {"token": token}
        self.assertDictEqual(response.json(), expected)


class LogoutTest(BaseTestCase):
    """
    Test logout
    """
    url = reverse_lazy("v1-logout")
    methods_not_allowed = ['get', 'post', 'put', 'patch', 'head', 'trace']

    def get_headers(self):
        return {
            "Content_Type": "application/json",
            "HTTP_AUTHORIZATION": "Token %s" % self.get_user_token("testlogout"),
        }

    def test_wrong_token(self):
        token = "Token x%s" % self.get_user_token("testuser")
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json().keys())
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)

    def test_success_response(self):
        token = "Token %s" % self.get_user_token("testuser")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 0)


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
        self.assertEqual(Token.objects.count(), 0)

    def test_success_response(self):
        self.get_user("user1")
        self.get_user_token("user2")
        data = {"username": "testuser", "password": "my_password"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Token.objects.count(), 2)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        expected = {"token": response.json().get("token")}
        self.assertDictEqual(response.json(), expected)
