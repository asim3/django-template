from django.test import TestCase
from backends.qr_code import (
    BytesQRCode,
    get_qr_code_image_path,
    add_url_qr_code,
)


class QRCodeTest(TestCase):
    def test_bytes_qr_code(self):
        qr_code = BytesQRCode()
        qr_code.add_data("test qr code")
        expected = 445
        actual = qr_code.get_image_bytes()
        self.assertEqual(expected, len(actual))
