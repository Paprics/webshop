import os

import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from cart.models import OrderModel

from .services_payments import get_line_items

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
key = os.getenv("STRIPE_KEY")
sekret_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = sekret_key


class PayOrderView(View):

    def get(self, request):
        order_id = request.GET.get('order_id')
        if not order_id:
            return HttpResponse('Invalid order', status=400)

        order = get_object_or_404(OrderModel, pk=order_id, customer=request.user)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = get_line_items(order),
            mode='payment',
            success_url='http://localhost:8000/payment/success/',
            cancel_url='http://localhost:8000/payment/cancel/',
            metadata={'order_id': str(order.id)},
        )

        return redirect(session.url)


class PayView(View):
    def get(self, request, *args, **kwargs):
        # Показываем простую страницу с кнопкой "Оплатить"
        return render(request, 'payment.html')

    def post(self, request, *args, **kwargs):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],

            # items = get_items(request),

            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Товар 1'},
                        'unit_amount': 1500,
                    },
                    'quantity': 2,
                },
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': 'Товар 2'},
                        'unit_amount': 999,
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
        return HttpResponseRedirect(session.url)


def success(request):
    return HttpResponse("✅ Оплата прошла успешно (sandbox)")


def cancel(request):
    return HttpResponse("❌ Оплата отменена")
