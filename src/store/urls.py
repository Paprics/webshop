from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
