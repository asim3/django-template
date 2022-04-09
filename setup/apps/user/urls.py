from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LogoutAPIView, RegisterAPIView


urlpatterns = [
    path('v1/user/login/', obtain_auth_token, name='v1-login'),
    path('v1/user/logout/', LogoutAPIView.as_view(), name='v1-logout'),
    path('v1/user/register/', RegisterAPIView.as_view(), name='v1-register'),
]
