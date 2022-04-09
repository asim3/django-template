from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('v1/auth/', obtain_auth_token),
]
