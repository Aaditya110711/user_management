from django.urls import path
from account.views import (
    UserRegistrationView, UserLoginView, UserProfileView, UserProfileUpdateView, PasswordResetConfirmView, PasswordResetRequestView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(),
         name='user-profile-update'),

    path('request-password-reset/', PasswordResetRequestView.as_view(),
         name='request-password-reset'),
    path('reset-password/', PasswordResetConfirmView.as_view(),
         name='reset-password'),
    path('reset-password/<str:token>/',
         PasswordResetConfirmView.as_view(), name='reset-password-confirm'),

]
