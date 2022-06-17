from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegistrationView,
    RegisterAPIView,
    UserInfoAPIView,
    CreateOneTimePasswordAPIView,
    ValidateOneTimePasswordAPIView
)

urlpatterns = [
    path('user/register/', RegistrationView.as_view(),
         name='user-register'),
    path('v1/user/', UserInfoAPIView.as_view(),
         name='v1-user-info'),
    path('v1/user/login/', TokenObtainPairView.as_view(),
         name='v1-user-login'),
    path('v1/user/otp/', CreateOneTimePasswordAPIView.as_view(),
         name='v1-user-otp-login'),
    path('v1/user/otp/validate/', ValidateOneTimePasswordAPIView.as_view(),
         name='v1-user-otp-validate'),
    path('v1/user/refresh/', TokenRefreshView.as_view(),
         name='v1-user-refresh'),
    path('v1/user/register/', RegisterAPIView.as_view(),
         name='v1-user-register'),
]
