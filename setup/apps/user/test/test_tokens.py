from django.test import TestCase
from django.contrib.auth.models import User, Permission

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.tokens import CustomizedRefreshToken


class CustomizedRefreshTokenTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "test_username",
            "test@user.com",
            "pass",
            first_name="my first name",
            last_name="my last name"
        )
        self.user.user_permissions.set(
            Permission.objects.filter(codename__startswith="view")
        )

    def test_refresh_token_payload(self):
        customized_token = CustomizedRefreshToken.for_user(self.user)
        token = RefreshToken(str(customized_token))
        self.assertEqual(token.payload["user_id"],
                         self.user.id)
        self.assertEqual(token.payload["username"],
                         self.user.get_username())
        self.assertEqual(token.payload["short_name"],
                         self.user.get_short_name())
        self.assertEqual(token.payload["full_name"],
                         self.user.get_full_name())
        self.assertEqual(token.payload["permissions"],
                         self.user.get_permissions_as_str())

    def test_access_token_payload(self):
        customized_token = CustomizedRefreshToken.for_user(self.user)
        token = AccessToken(str(customized_token.access_token))
        self.assertEqual(token.payload["user_id"],
                         self.user.id)
        self.assertEqual(token.payload["username"],
                         self.user.get_username())
        self.assertEqual(token.payload["short_name"],
                         self.user.get_short_name())
        self.assertEqual(token.payload["full_name"],
                         self.user.get_full_name())
        self.assertEqual(token.payload["permissions"],
                         self.user.get_permissions_as_str())

    def test_access_token_payload_from_refresh_token(self):
        customized_token = CustomizedRefreshToken.for_user(self.user)
        refresh = RefreshToken(str(customized_token))
        token = AccessToken(str(refresh.access_token))
        self.assertEqual(token.payload["user_id"],
                         self.user.id)
        self.assertEqual(token.payload["username"],
                         self.user.get_username())
        self.assertEqual(token.payload["short_name"],
                         self.user.get_short_name())
        self.assertEqual(token.payload["full_name"],
                         self.user.get_full_name())
        self.assertEqual(token.payload["permissions"],
                         self.user.get_permissions_as_str())
