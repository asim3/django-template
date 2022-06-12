from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from user.models import OneTimePassword

from .base import BaseTestCase


class OneTimePasswordModelTest(BaseTestCase):
    """
    Test OneTimePassword Model
    """

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

    def test_delete_old(self):
        OneTimePassword.objects.create(phone="966512345678", key="1234")
        OneTimePassword.objects.create(phone="966587654321", key="5555")
        OneTimePassword.objects.create(phone="001", key="1", is_verified=True)
        OneTimePassword.objects.create(phone="002", key="2", is_verified=True)
        OneTimePassword.objects.create(phone="003", key="3", is_verified=True)
        OneTimePassword.objects.create(phone="004", key="4", is_verified=True)

        self.assertEqual(OneTimePassword.objects.count(), 6)
        OneTimePassword.objects.filter(is_verified=True).delete()
        self.assertEqual(OneTimePassword.objects.count(), 2)


class OneTimePasswordViewTest(BaseTestCase):
    """
    Test One Time Password View
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
