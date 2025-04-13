from django.urls import path,include
from .views import HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path("api/v1/", include('product.api.v1.urls')),
]