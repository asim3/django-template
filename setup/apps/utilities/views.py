from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from user.serializers import RegisterSerializer


class CaptchaAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    # def post(self, request):
    #     key = str(uuid.uuid4())
    #     value = utils.random_char_challenge(api_settings.CAPTCHA_LENGTH)
    #     cache_key = utils.get_cache_key(key)
    #     cache.set(cache_key, value, api_settings.CAPTCHA_TIMEOUT)

    #     # generate image
    #     image_bytes = captcha.generate_image(value)
    #     image_b64 = base64.b64encode(image_bytes)

    #     data = {
    #         api_settings.CAPTCHA_KEY: key,
    #         api_settings.CAPTCHA_IMAGE: image_b64,
    #         'image_type': 'image/png',
    #         'image_decode': 'base64'
    #     }
    #     return response.Response(data)
