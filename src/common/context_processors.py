from cart.views import get_cart


def category_processor_nested(request):
    from store.models import CategoryModelMPTT

    # categories_nested = CategoryModelMPTT.objects.root_nodes()  # N+1 query
    categories_nested = CategoryModelMPTT.objects.root_nodes().prefetch_related(
        "children"
    )  # TODO: check optimiz.
    cart = get_cart(request)
    cart_items_count = sum(item.quantity for item in cart.items)
    return {
        "categories_nested": categories_nested,
        "cart_items_count": cart_items_count,
    }
