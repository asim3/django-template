from django.urls import path

from .views import (
    RegistrationView,
    SendEmailVerificationView,
    EmailVerificationConfirmView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    UserInfoAPIView,
    CreateOneTimePasswordAPIView,
    ValidateOneTimePasswordAPIView,
    RegisterAPIView,
    TokenLoginAPIView,
    TokenRefreshAPIView,
)


urlpatterns = [
    path('user/register/', RegistrationView.as_view(),
         name='user-register'),
    path('user/email-verification/', SendEmailVerificationView.as_view(),
         name='user-email-verification'),
    path('user/email-verification/<uidb64>/<token>/',
         EmailVerificationConfirmView.as_view(),
         name='user-email-verification-confirm'),

    # reset password
    path('user/password_reset/', UserPasswordResetView.as_view(),
         name='admin_password_reset'),
    path('user/password_reset/done/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('user/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('user/reset/done/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # api v1
    path('v1/user/', UserInfoAPIView.as_view(),
         name='v1-user-info'),
    path('v1/user/login/', TokenLoginAPIView.as_view(),
         name='v1-user-login'),
    path('v1/user/otp/', CreateOneTimePasswordAPIView.as_view(),
         name='v1-user-otp-login'),
    path('v1/user/otp/validate/', ValidateOneTimePasswordAPIView.as_view(),
         name='v1-user-otp-validate'),
    path('v1/user/refresh/', TokenRefreshAPIView.as_view(),
         name='v1-user-refresh'),
    path('v1/user/register/', RegisterAPIView.as_view(),
         name='v1-user-register'),
]
