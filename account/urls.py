from django.urls import path
from account.views import *


urlpatterns = [
    path("register-view/", RegistrationView.as_view(), name="register-view"),
    path("signup-view/", SignupView.as_view(), name="signup-view/"),
]