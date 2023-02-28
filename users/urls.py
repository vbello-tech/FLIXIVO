from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name = "user"


urlpatterns = [
    path('login/', LoginView.as_view(template_name='registrations/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', signup_view, name="sign_up"),
    path('change-password/', change_password, name="change_password"),
    path('reset-password/', PasswordResetView.as_view(
        template_name='registrations/password_reset.html',
        success_url=reverse_lazy('user:password_reset_done')
    ), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/(<uidb64>)-(<token>)/', PasswordResetConfirmView.as_view(
        template_name='registrations/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete')
    ), name="password_reset_confirm"),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'),
         name="password_reset_complete"),
    path('user/follow/<int:pk>/', follow, name="follow"),
    path('detail/<int:pk>/', ProfileView.as_view(), name="profile"),
    path('profile/', profile, name="user-profile"),
    path('profile/edit/', ProfileUpdate.as_view(), name="edit_profile"),
]
