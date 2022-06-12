from django.test import TestCase
from django.conf import settings
from backends.utils import (
    generate_random_key,
    generate_OTP_key,
    clean_arabic_digits,
    send_sms_message,
)


class UtilsTest(TestCase):
    def test_generate_random_key(self):
        self.assertEqual(len(generate_random_key()), 100)
        self.assertEqual(type(generate_random_key()), str)
        self.assertEqual(len(generate_random_key(length=50)), 50)

    def test_generate_OTP_key(self):
        self.assertEqual(type(generate_OTP_key()), str)
        self.assertEqual(len(generate_OTP_key()), settings.OTP_MAX_LENGTH)

    def test_clean_arabic_digits(self):
        self.assertEqual(clean_arabic_digits("0123456789"), "0123456789")
        self.assertEqual(clean_arabic_digits(
            "٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩"), "0 1 2 3 4 5 6 7 8 9")
        self.assertEqual(clean_arabic_digits("٠١٢٣٤٥٦٧٨٩"), "0123456789")
        self.assertEqual(clean_arabic_digits("٠١٢٣٤A٥٦٧B٨٩"), "01234A567B89")
        self.assertEqual(clean_arabic_digits("٥٦٧٨٩٠١٢٣٤"), "5678901234")
        self.assertEqual(clean_arabic_digits("٠١٢٣٤s٦٧٨٩"), "01234s6789")
        self.assertEqual(clean_arabic_digits(
            "٠١٢٣٤إختبار٥٦٧٨٩"), "01234إختبار56789")
        self.assertEqual(clean_arabic_digits(
            "٠١٢٣٤ إختبار ٥٦٧٨٩"), "01234 إختبار 56789")
        self.assertEqual(clean_arabic_digits(
            "٠١٢٣٤ test ٥٦٧٨٩"), "01234 test 56789")

    def test_send_sms_message(self):
        with self.assertRaises(TypeError):
            send_sms_message()
        self.assertIsNone(send_sms_message(""))
