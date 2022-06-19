from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from user.models import Profile

from .base import BaseTestCase


class ProfileTest(BaseTestCase):
    """
    Test Profile Model
    """

    def test_add(self):
        user = User.objects.create(username="new-user")
        profile = Profile.objects.create(user=user)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.phone, None)
        self.assertEqual(profile.is_email_verified, False)

    def test_update(self):
        user_1 = self.get_user("otp-user1", phone="966512345678")
        user_2 = self.get_user("otp-user2", phone="966587654321")
        self.assertEqual(Profile.objects.count(), 2)
        profile = Profile.objects.get(user=user_1)
        new_phone = "96650000"
        profile.phone = new_phone
        profile.save()
        new_profile = Profile.objects.get(phone=new_phone)
        self.assertEqual(new_profile.user, user_1)
        self.assertEqual(new_profile.is_email_verified, False)
