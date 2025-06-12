# cart.py
from store.models import ProductModel


class ShoppingCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart_data", None)
        if cart is None:
            cart = self.session["cart_data"] = {}
        self.cart = cart

    def add(self, product_slug, quantity=1):
        if product_slug in self.cart:
            self.cart[product_slug] += quantity
        else:
            self.cart[product_slug] = quantity
        self.session.modified = True

    @property
    def items(self):
        slugs = self.cart.keys()
        products = ProductModel.objects.filter(slug__in=slugs, is_active=True)
        cart_items = []
        for product in products:
            product.quantity = self.cart.get(product.slug, 1)
            cart_items.append(product)
        return cart_items

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = quantity
            self.session.modified = True

    def clear(self):
        self.session["cart_data"] = {}
        self.session.modified = True
