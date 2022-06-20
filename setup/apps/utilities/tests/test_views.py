from django.test import TestCase
from utilities.views import DownloadView


class DownloadViewTest(TestCase):
    def test_get_file_name(self):
        expected = str
        actual = DownloadView().get_file_name()
        self.assertEqual(expected, type(actual))

    def test_get_binary_content(self):
        with self.assertRaisesMessage(ValueError, "Please override this method!"):
            DownloadView().get_binary_content(context={})
