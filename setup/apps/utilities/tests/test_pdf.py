from django.test import TestCase
from utilities.pdf import PDF


class PDFTest(TestCase):
    def test_pdf_output(self):
        expected = 18000
        pdf = PDF()
        pdf.write(50, 'www.fpdf.org')
        actual = pdf.output(dest="s")
        self.assertLess(len(actual), expected)
