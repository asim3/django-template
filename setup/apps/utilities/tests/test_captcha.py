from django.test import TestCase
from django.urls import reverse_lazy


class RegistrationTest(TestCase):
    """
    Test Registration
    """
    url = reverse_lazy("v1-captcha")
    methods_not_allowed = ['patch', 'delete', 'trace']

    def test_empty_request(self):
        response = self.client.get(self.url)
