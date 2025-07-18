from cart import cart_logic


def get_cart(request):
    if request.user.is_authenticated:
        return cart_logic.ShoppingCartUser(request)
    else:
        return cart_logic.ShoppingCartAnonymousUser(request)
