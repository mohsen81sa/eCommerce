from django.urls import path
from account.views import *


urlpatterns = [
    path("send-email-verification-view/", SendEmailVerificationView.as_view(), name="send-email-verification"),
    path("register-view/", RegistrationView.as_view(), name="register-view"),
    path("signup-view/", SignupView.as_view(), name="signup-view/"),
    path("login-view/", LoginView.as_view(), name="login-view/"),
    path("get-profile-view/", GetUserProfileView.as_view()),
]
