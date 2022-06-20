from django.views.generic.base import TemplateView
from django.http import FileResponse
from django.utils import timezone

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from user.serializers import RegisterSerializer


class DownloadView(TemplateView):
    file_name = None
    is_attachment = True

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return FileResponse(
            streaming_content=self.get_binary_content(context),
            as_attachment=self.is_attachment,
            filename=self.get_file_name(),
            **response_kwargs)

    def get_file_name(self):
        if self.file_name:
            return self.file_name
        return "file-%s.pdf" % timezone.now().strftime("%d-%m-%Y-%H-%M-%S")

    def get_binary_content(self, context):
        raise ValueError("Please override this method!")


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
