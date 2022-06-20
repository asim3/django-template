from django.urls import path

from .views import (
    CaptchaAPIView,
)


urlpatterns = [
    path('v1/captcha/', CaptchaAPIView.as_view(), name='v1-captcha'),
]
