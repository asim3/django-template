from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home/home.html"


class DocumentationView(TemplateView):
    template_name = 'api/swagger-ui.html'


class SchemaView(TemplateView):
    template_name = 'api/openapi-schema.yaml'
    content_type = "text/plain"
