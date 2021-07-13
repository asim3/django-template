from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView


urlpatterns = i18n_patterns(
    path('', include('products.urls')),
    path('admin/', admin.site.urls),
)


urlpatterns += [
    path('', RedirectView.as_view(pattern_name='home')),
]
