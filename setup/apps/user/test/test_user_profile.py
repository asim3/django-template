from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Permission, Group

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


class UserPermissionsTest(BaseTestCase):
    """
    Test User get all permissions as str
    """

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

    def test_permission_list_as_str(self):
        permissions = [obj for obj in self.user.get_all_permissions()]
        user_permissions = ",".join(permissions)
        self.assertEqual(self.user.get_permissions_as_str(), user_permissions)
