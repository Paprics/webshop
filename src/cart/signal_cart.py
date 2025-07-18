from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from cart.views import get_cart


@receiver(user_logged_in)
def login_merge_cart(sender, request, user, **kwargs):
    cart = get_cart(request)
    cart.merge_session_cart()
    request.session["merge_cart_after_login"] = True
