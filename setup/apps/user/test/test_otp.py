from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from user.models import OneTimePassword
from utilities.utils import clean_phone_number
from utilities.tests.mock_patch import patch, MockedSMSRequests

from .base import BaseTestCase


class OneTimePasswordModelTest(BaseTestCase):
    """
    Test OneTimePassword Model
    """
    expired_time = timezone.now() - timezone.timedelta(minutes=6)

    def test_add(self):
        phone = "966512345678"
        OneTimePassword.objects.create(phone=phone, key="1234")
        self.assertEqual(OneTimePassword.objects.count(), 1)

    def test_add_multiple(self):
        phone_1 = "966512345678"
        phone_2 = "966587654321"
        OneTimePassword.objects.create(phone=phone_1, key="1234")
        OneTimePassword.objects.create(phone=phone_2, key="5678")
        self.assertEqual(OneTimePassword.objects.count(), 2)

    def test_is_datetime_valid(self):
        OneTimePassword.objects.create(phone="9661", key="1234")
        OneTimePassword.objects.create(phone="9662", key="1234")
        OneTimePassword.objects.create(phone="9663", key="1234")
        OneTimePassword.objects.create(phone="9664", key="1234")
        OneTimePassword.objects.all().update(created_on=self.expired_time)
        OneTimePassword.objects.create(phone="9665", key="1234")
        self.assertEqual(OneTimePassword.objects.count(), 5)
        self.assertFalse(OneTimePassword.objects.first().is_datetime_valid())
        self.assertTrue(OneTimePassword.objects.last().is_datetime_valid())
        self.assertEqual(OneTimePassword.objects.count(), 1)

    def test_delete_expired(self):
        OneTimePassword.objects.create(phone="9661", key="1234")
        OneTimePassword.objects.create(phone="9662", key="1234")
        OneTimePassword.objects.create(phone="9663", key="1234")
        OneTimePassword.objects.create(phone="9664", key="1234")
        OneTimePassword.objects.all().update(created_on=self.expired_time)
        OneTimePassword.objects.create(phone="9665", key="1234")
        self.assertEqual(OneTimePassword.objects.count(), 5)
        OneTimePassword.delete_expired()
        self.assertEqual(OneTimePassword.objects.count(), 1)


@patch("utilities.utils.requests", MockedSMSRequests)
class CreateOneTimePasswordAPIViewTest(BaseTestCase):
    """
    Test Create One Time Password APIView
    """
    url = reverse_lazy("v1-user-otp-login")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json().keys())
        self.assertEqual(OneTimePassword.objects.count(), 0)

    def test_phone_not_found(self):
        self.get_user("otp-user", phone="966512345678")
        data = {"phone": "12321"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        error_text = response.json().get("phone")[0]
        self.assertEqual(error_text, _("This phone number is not registered"))
        self.assertEqual(OneTimePassword.objects.count(), 0)

    def test_OTP_duplicate_phone(self):
        self.get_user("otp-user1", phone="966512345678")
        self.get_user("otp-user2", phone="966587654322")
        self.get_user("otp-user3", phone="966587654323")
        response = self.client.post(self.url, data={"phone": "966512345678"})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.post(self.url, data={"phone": "966587654322"})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.post(self.url, data={"phone": "966587654323"})
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        response = self.client.post(self.url, data={"phone": "966512345678"})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json().keys())
        self.assertEqual(OneTimePassword.objects.count(), 3)

    def test_success_response(self):
        self.get_user("otp-user1", phone="966512345678")
        data = {"phone": "966512345678"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(OneTimePassword.objects.count(), 1)

    def test_multiple_success_response(self):
        self.get_user("otp-user1", phone="966512345678")
        self.get_user("otp-user2", phone="966587654321")
        data = {"phone": "966512345678"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        data = {"phone": "966587654321"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(OneTimePassword.objects.count(), 2)

    def test_clean_phone_number(self):
        phone_list = [
            ("0512345678", "966512345678"),
            ("587654321", "966587654321"),
            ("966500", "966500"),
            ("0503", "966503"),
            ("5123456789", "5123456789"),
            ("51234567", "51234567"),
            ("12345678", "12345678"),
            ("+966504", "966504"),
        ]
        for actual, expected in phone_list:
            self.get_user(phone=expected)
            response = self.client.post(self.url, data={"phone": actual})
            self.assertEqual(
                response.status_code,
                HTTP_201_CREATED,
                msg=actual)
            try:
                otp = OneTimePassword.objects.get(phone=expected)
                self.assertEqual(otp.phone, expected)
            except OneTimePassword.DoesNotExist:
                self.assertEqual(actual + "x", expected)


class ValidateOneTimePasswordAPIViewTest(BaseTestCase):
    """
    Test Validate One Time Password View
    """
    url = reverse_lazy("v1-user-otp-validate")
    methods_not_allowed = ['get', 'put', 'patch', 'delete', 'head', 'trace']
    users_list = [
        {"phone": "0512345678", "token": "0001"},
        {"phone": "587654321", "token": "0002"},
        {"phone": "966500", "token": "3344"},
        {"phone": "0503", "token": "5566"},
        {"phone": "5123456789", "token": "7777"},
        {"phone": "51234567", "token": "8888"},
        {"phone": "12345678", "token": "9999"},
        {"phone": "+966504", "token": "1000"},
    ]

    def add_multiple_otp(self):
        for item in self.users_list:
            phone = clean_phone_number(item["phone"])
            self.get_user(phone=phone)
            OneTimePassword.objects.create(
                phone=phone, key=item["token"])

    def test_empty_request(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn('phone', response.json().keys())
        self.assertIn('token', response.json().keys())
        self.assertEqual(OneTimePassword.objects.count(), 0)

    def test_phone_not_found(self):
        self.add_multiple_otp()
        data = {"phone": "12321", "token": "1111"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        error_text = response.json().get("non_field_errors")[0]
        self.assertEqual(error_text, _(
            "The phone or token you entered are not correct"))
        self.assertEqual(OneTimePassword.objects.count(), len(self.users_list))

    def test_token_not_found(self):
        self.add_multiple_otp()
        data = {"phone": "0503", "token": "0503"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        error_text = response.json().get("non_field_errors")[0]
        self.assertEqual(error_text, _(
            "The phone or token you entered are not correct"))
        self.assertEqual(OneTimePassword.objects.count(), len(self.users_list))

    def test_success_response(self):
        self.add_multiple_otp()
        for user_id, data in enumerate(self.users_list, 1):
            response = self.client.post(self.url, data=data)
            self.assertEqual(response.status_code, HTTP_201_CREATED, msg=data)
            refresh = response.json().get("refresh")
            access = response.json().get("access")
            self.assertEqual(RefreshToken(refresh).get("user_id"), user_id)
            self.assertEqual(AccessToken(access).get("user_id"), user_id)
            self.assertEqual(
                OneTimePassword.objects.count(), len(self.users_list) - user_id)
        self.assertEqual(OneTimePassword.objects.count(), 0)
