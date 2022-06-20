from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf import settings


admin.site.site_header = _("My App")
admin.site.site_title = _("Admin")
admin.site.index_title = _("Controls")
admin.site.empty_value_display = _("empty")


urlpatterns = i18n_patterns(
    path('', include('user.urls')),
    path('admin/', admin.site.urls),
    path('', include('utilities.urls')),
    path('', include('home.urls')),
)


urlpatterns += [
    path('captcha/', include('captcha.urls')),
    path('', RedirectView.as_view(pattern_name='home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
