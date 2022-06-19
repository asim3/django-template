from django.test import TestCase
from django.conf import settings
from backends.tests.mock_patch import patch, MockedSMSRequests
from backends.utils import (
    clean_phone_number,
    clean_arabic_digits,
    generate_random_key,
    generate_random_name,
    generate_OTP_key,
    send_sms_message,
    SMS_Error,
)


@patch("backends.utils.requests", MockedSMSRequests)
class UtilsTest(TestCase):
    def test_generate_random_key(self):
        self.assertEqual(len(generate_random_key()), 100)
        self.assertEqual(type(generate_random_key()), str)
        self.assertEqual(len(generate_random_key(length=50)), 50)

    def test_generate_random_name(self):
        self.assertEqual(len(generate_random_name()), 10)
        self.assertEqual(type(generate_random_name()), str)
        self.assertEqual(len(generate_random_name(length=50)), 50)

    def test_generate_OTP_key(self):
        self.assertEqual(type(generate_OTP_key()), str)
        self.assertEqual(len(generate_OTP_key()), settings.OTP_MAX_LENGTH)

    def test_clean_saudi_phone_number(self):
        self.assertEqual(clean_phone_number("+966500"), "966500")
        self.assertEqual(clean_phone_number("966500"), "966500")
        self.assertEqual(clean_phone_number("0500"), "966500")
        self.assertEqual(clean_phone_number("512345678"), "966512345678")
        self.assertEqual(clean_phone_number("512345678"), "966512345678")

    def test_clean_other_phone_number(self):
        self.assertEqual(clean_phone_number("5500"), "5500")
        self.assertEqual(clean_phone_number("66500"), "66500")
        self.assertEqual(clean_phone_number("001500"), "1500")
        self.assertEqual(clean_phone_number("+1500"), "1500")
        self.assertEqual(clean_phone_number("1500"), "1500")
        self.assertEqual(clean_phone_number("52345678"), "52345678")
        self.assertEqual(clean_phone_number("5234567890"), "5234567890")
        self.assertEqual(clean_phone_number("12Abc345"), "12Abc345")
        self.assertEqual(clean_phone_number("xyz"), "xyz")
        self.assertEqual(clean_phone_number("إختبار"), "إختبار")

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

    def test_send_sms_message_error(self):
        with self.assertRaises(TypeError):
            send_sms_message()
        with self.assertRaises(TypeError):
            send_sms_message("phone")
        with self.assertRaises(SMS_Error):
            send_sms_message("not_digit", "1234", raise_exception=True)

    def test_send_sms_message(self):
        self.assertTrue(send_sms_message("966500", "text"))
        self.assertFalse(send_sms_message("phone", "text"))
        self.assertFalse(send_sms_message(
            "not_digit", "text", raise_exception=False))
