from django.test import TestCase
from PIL import Image
from backends.images import (
    resize_image,
    resize_image_as_bytes_io,
    resize_image_field,
    add_resize_image_signal,
)


class ImagesTest(TestCase):
    def test_resize_image(self):
        expected_size = (120, 41)
        with Image.open("./backends/tests/data/django-logo-positive.png"
                        ) as image_file:
            actual = resize_image(image_file, new_width=120)
            self.assertEqual(expected_size, actual.size)

    def test_resize_image_as_bytes_io(self):
        with Image.open("./backends/tests/data/django-logo-positive.png"
                        ) as image_file:
            actual = resize_image_as_bytes_io(image_file, new_width=24)
            self.assertLess(actual.size, 1000)

    def test_resize_image_field(self):
        image_path = "./backends/tests/data/django-logo-positive.png"
        actual = resize_image_field(image_path, new_width=24)
        self.assertLess(actual.size, 1000)
