from django.urls import path
from .views import HomeView, DocumentationView, SchemaView


urlpatterns = [
    path('schema/', SchemaView.as_view(), name='api-schema'),
    path('docs/', DocumentationView.as_view(), name='api-docs'),
    path('', HomeView.as_view(), name="home"),
]
