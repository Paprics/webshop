# cart.py
from store.models import ProductModel


class ShoppingCart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart_data", None)
        if cart is None:
            cart = self.session["cart_data"] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.session.modified = True

    @property
    def items(self):
        ids = self.cart.keys()
        products = ProductModel.objects.filter(id__in=ids, is_active=True)
        cart_items = []
        for product in products:
            product.quantity = self.cart.get(str(product.id), 1)
            cart_items.append(product)
        return cart_items

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            if self.cart[product_id] > 1:
                self.cart[product_id] -= 1
            else:
                del self.cart[product_id]
            self.session.modified = True


    def get_total_cart_price(self):
        return sum(product.price * product.quantity for product in self.items)

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
