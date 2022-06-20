from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED

from utilities.utils import generate_random_name
from user.models import Profile


class BaseTestCase(TestCase):
    methods_not_allowed = None
    requires_authorization = False

    def get_headers(self):
        if self.requires_authorization:
            return {
                "Content_Type": "application/json",
                "HTTP_AUTHORIZATION": self.get_user_bearer_head("auth_user"),
            }
        return {"Content_Type": "application/json"}

    def test_method_not_allowed(self):
        if self.methods_not_allowed:
            for method in self.methods_not_allowed:
                response = getattr(self.client, method)(
                    self.url, **self.get_headers())
                message = "%s method" % method
                self.assertEqual(response.status_code,
                                 HTTP_405_METHOD_NOT_ALLOWED, message)

    def add_new_user(self, data):
        user = User.objects.create(username=data['username'])
        if data.get('password'):
            user.set_password(data['password'])
            user.save()
        return user

    def get_user(self, username=None, phone=None):
        if not username:
            username = generate_random_name()
        user, _ = User.objects.get_or_create(username=username)
        if phone:
            Profile.objects.get_or_create(user=user, phone=phone)
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

    def get_user_bearer_head(self, username):
        refresh = self.get_user_token(username)
        return "Bearer %s" % refresh.get("access")
