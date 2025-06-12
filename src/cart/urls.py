from django.urls import path

from cart import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<slug:product_slug>/", views.add_to_cart, name="add_to_cart"),
    # path('cart/delete/<int:pk>/', views.delete_from_cart, name="delete_from_cart" ),
]
