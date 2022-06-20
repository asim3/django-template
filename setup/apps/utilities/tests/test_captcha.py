from django.urls import reverse_lazy
from rest_framework.status import HTTP_200_OK

from .base import BaseTestCase


class CaptchaTest(BaseTestCase):
    """
    Test Captcha
    """
    url = reverse_lazy("v1-captcha")
    methods_not_allowed = ['post', 'put', 'patch', 'delete', 'trace']

    def test_empty_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn('key', response.json().keys())
        self.assertIn('image_url', response.json().keys())
        self.assertIn('large_image_url', response.json().keys())
