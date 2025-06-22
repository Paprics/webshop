from django.urls import path

from cart import views

app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("delete/<int:product_pk>/", views.remove_cart, name="remove_cart"),
    path("order_review/", views.OrderReviewView.as_view(), name="order_review"),
    path("order_create/", views.OrderCreateView.as_view(), name="order_create"),
]
