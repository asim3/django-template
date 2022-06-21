from django.views.generic.base import TemplateView
from django.http import FileResponse
from django.utils import timezone
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from .serializers import CaptchaSerializer


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


class CaptchaAPIView(RetrieveAPIView):
    """
    Generate a new CAPTCHA challenge that humans can pass.

    Valid for 5 minutes. 
    """
    permission_classes = [AllowAny]
    serializer_class = CaptchaSerializer

    def get_object(self):
        new_key = CaptchaStore.pick()
        return {
            "key": new_key,
            "image_url": captcha_image_url(new_key),
            "large_image_url": reverse("captcha-image-2x", args=[new_key]),
        }
