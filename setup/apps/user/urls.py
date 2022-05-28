from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterAPIView


urlpatterns = [
    path('v1/user/login/', TokenObtainPairView.as_view(), name='v1-login'),
    path('v1/user/refresh/', TokenRefreshView.as_view(), name='v1-refresh'),
    path('v1/user/register/', RegisterAPIView.as_view(), name='v1-register'),
]
