from django.test import TestCase
from utilities.zip import extract_zip_file


class ExtractZipTest(TestCase):
    def test_extract_zip_file(self):
        expected = "django-logo-positive.png"
        file_path = "./utilities/tests/data/django-logo.zip"
        actual = extract_zip_file(file_path)
        self.assertEqual(expected, actual[0][0])

    def test_extract_error(self):
        with self.assertRaises(FileNotFoundError):
            extract_zip_file("none")
