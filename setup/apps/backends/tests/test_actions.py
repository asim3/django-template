from django.test import TestCase
from django.contrib.auth.models import User
from backends.actions import (
    export_to_excel_file,
)


class ActionsTest(TestCase):
    def test_export_to_excel_file(self):
        admin_class = ""
        request = ""
        queryset = User.objects.all()

        expected = 200
        actual = export_to_excel_file(admin_class, request, queryset)
        self.assertEqual(expected, actual.status_code)
