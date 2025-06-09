from django.urls import path

from cart.views import CartDetailView

app_name = "cart"

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
]
