from django.test import TestCase
from django.contrib.auth.models import User

from backends.tokens import PasswordResetTokenGenerator, EmailVerificationTokenGenerator


class TokensTest(TestCase):
    def test_password_generator_key_salt(self):
        pass_generator = PasswordResetTokenGenerator()
        email_generator = EmailVerificationTokenGenerator()
        user = User.objects.create_user(
            "test_username", "test@user.com", "pass")
        tokens = [
            pass_generator.make_token(user),
            pass_generator.make_token(user),
            pass_generator.make_token(user),
            pass_generator.make_token(user),
        ]
        for token in tokens:
            self.assertFalse(email_generator.check_token(user, token))
            self.assertTrue(pass_generator.check_token(user, token))

    def test_email_generator_key_salt(self):
        pass_generator = PasswordResetTokenGenerator()
        email_generator = EmailVerificationTokenGenerator()
        user = User.objects.create_user(
            "test_username", "test@user.com", "pass")
        tokens = [
            email_generator.make_token(user),
            email_generator.make_token(user),
            email_generator.make_token(user),
            email_generator.make_token(user),
        ]
        for token in tokens:
            self.assertFalse(pass_generator.check_token(user, token))
            self.assertTrue(email_generator.check_token(user, token))
