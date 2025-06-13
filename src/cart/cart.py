class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart", None)
        if cart is None:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.session.modified = True

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

    def items(self):
        return self.cart.items()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True
