from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from store.models import ProductModel

from .cart_logic import ShoppingCart


def remove_cart(request, product_pk):
    cart = ShoppingCart(request)
    cart.remove(product_id=product_pk)

    return redirect("cart:cart_detail")


def add_to_cart(request, product_id):
    cart = ShoppingCart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.add(product.id)
    return redirect("cart:cart_detail")


class CartDetailView(TemplateView):
    template_name = "cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = ShoppingCart(self.request)
        context["cart_items"] = cart.items
        return context
