from django.test import TestCase
from utilities.storages import (
    PublicMediaStorage,
    FontMediaStorage,
    PrivateMediaStorage,
)


class StorageTest(TestCase):
    def test_public_media(self):
        actual = PublicMediaStorage()
        self.assertEqual(actual.location, "media/public")
        self.assertEqual(actual.default_acl, None)

    def test_public_font(self):
        actual = FontMediaStorage()
        self.assertEqual(actual.location, "media/font")
        self.assertEqual(actual.default_acl, None)

    def test_private_media(self):
        actual = PrivateMediaStorage()
        self.assertEqual(actual.location, "media/private")
        self.assertEqual(actual.default_acl, "private")
