from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'media/public'
    file_overwrite = False


class FontMediaStorage(S3Boto3Storage):
    location = 'media/font'
    file_overwrite = True


class PrivateMediaStorage(S3Boto3Storage):
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
    signature_version = 's3v4'


# class MyPhoto(Model):
#   upload = FileField(storage=PrivateMediaStorage())
