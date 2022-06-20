from qrcode import QRCode
from io import BytesIO
from tempfile import NamedTemporaryFile


class BytesQRCode(QRCode):
    def get_image_bytes(self, **kwargs):
        pil_image = super().make_image(**kwargs)
        with BytesIO() as bytes_file:
            pil_image.save(bytes_file, format='PNG')
            return bytes_file.getvalue()


def get_qr_code_image_path(text):
    my_qr_code = BytesQRCode()
    my_qr_code.add_data(text)

    temporary_file = NamedTemporaryFile(suffix=".png", delete=False)
    temporary_file.write(my_qr_code.get_image_bytes())
    temporary_file.seek(0)

    return temporary_file.name


def add_url_qr_code(my_pdf, url):
    my_qr_code = BytesQRCode()
    my_qr_code.add_data(url)

    temporary_file = NamedTemporaryFile(suffix=".png")
    temporary_file.write(my_qr_code.get_image_bytes())
    temporary_file.seek(0)

    image_path = temporary_file.name
    image_width = 250
    page_width_a4 = 595.28
    x_coordinate = (page_width_a4 / 2) - (image_width / 2)

    my_pdf.image(image_path, x=x_coordinate, w=image_width)
