from django.views.generic.base import TemplateView
from django.http import FileResponse
from django.utils import timezone


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
