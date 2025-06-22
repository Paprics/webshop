from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.models import CustomerUser
from store.models import ProductModel

from .cart_logic import ShoppingCartAnonymousUser, ShoppingCartUser
from .models import OrderItemModel, OrderModel


def get_cart(request):
    if request.user.is_authenticated:
        return ShoppingCartUser(request)
    else:
        return ShoppingCartAnonymousUser(request)


class OrderCreateView(View):

    def post(self, request, *args, **kwargs):
        cart = get_cart(request)

        with transaction.atomic():
            order_items = []
            order = OrderModel.objects.create(customer=request.user)

            for product in cart:
                order_item = OrderItemModel(
                    order=order,
                    product=ProductModel.objects.get(pk=product.pk),
                    quantity=product.quantity,
                    price_at_order_time=product.price,
                )
                order_items.append(order_item)
            OrderItemModel.objects.bulk_create(order_items)

            cart.clear()
        return redirect("common:index")


def remove_cart(request, product_pk):
    cart = get_cart(request)
    cart.remove(product_id=product_pk)

    return redirect("cart:cart_detail")


def add_to_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(ProductModel, id=product_id)
    cart.add(product.id)
    return redirect("cart:cart_detail")


class CartDetailView(TemplateView):
    template_name = "cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_cart(self.request)
        items = cart.items
        for item in items:
            item.total_price = item.price * item.quantity
        context["cart_items"] = items
        context["cart_total_price"] = cart.get_total_cart_price()

        return context


class OrderReviewView(TemplateView):
    template_name = "order_confirm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_items = get_cart(self.request)
        user = CustomerUser.objects.select_related("profile").get(pk=self.request.user.pk)

        context["cart_items"] = cart_items
        context["user"] = user

        return context
