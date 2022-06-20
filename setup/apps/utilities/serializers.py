from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer, CharField


class CaptchaSerializer(Serializer):
    key = CharField()
    image_url = CharField()
    large_image_url = CharField()
