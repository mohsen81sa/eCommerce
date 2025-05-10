from django.urls import path
from .views import *


urlpatterns = [
    path("payment/", PaymentView.as_view()),
]