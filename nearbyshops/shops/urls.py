from django.urls import path
from shops.views import ShopListAPIView

urlpatterns = [
    path('', ShopListAPIView.as_view())
]