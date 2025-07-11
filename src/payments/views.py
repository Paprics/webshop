import os

import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from cart.models import OrderModel

from .services_payments import get_line_items

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


class PayOrderView(View):

    def get(self, request):
        order_id = request.GET.get("order_id")
        if not order_id:
            return HttpResponse("Invalid order", status=400)

        order = get_object_or_404(OrderModel, pk=order_id, customer=request.user)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=get_line_items(order),
            mode="payment",
            success_url="http://localhost:8000/payment/success/",
            cancel_url=f"http://localhost:8000/payment/canceled/{order.id}/",
            metadata={"order_id": str(order.id)},
        )

        return redirect(session.url)

class CancelOrderView(View):
    template_name = "cancel.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")

        if order_id:
            order = get_object_or_404(OrderModel, pk=order_id, customer=request.user)
            order.status = 'cancelled'
            order.save()

        return render(request, self.template_name)

