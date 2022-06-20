from django.utils.translation import gettext_lazy as _
from django.test import TestCase
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class BaseTestCase(TestCase):
    # methods_not_allowed = ['get', 'post', 'put', 'patch', 'delete', 'head', 'trace']
    methods_not_allowed = None

    def test_method_not_allowed(self):
        if self.methods_not_allowed:
            for method in self.methods_not_allowed:
                response = getattr(self.client, method)(self.url)
                message = "%s method" % method
                self.assertEqual(response.status_code,
                                 HTTP_405_METHOD_NOT_ALLOWED, message)
