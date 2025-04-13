from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

app_name = "api-v1"


router = DefaultRouter()
router.register('products', ProductViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     # path('products/', ProductListView.as_view(), name='product-list'),
# ]