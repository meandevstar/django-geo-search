from django.urls import path
from shops import views

urlpatterns = [
    path('', views.ShopListAPIView.as_view())
]