from cart.models import StoreCart
from store.models import ProductModel


class ShoppingCartAnonymousUser:
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


class ShoppingCartUser:
    def __init__(self, request):
        self.user = request.user
        self.session = request.session

    def merge_session_cart(self):
        session_cart = self.session.get("cart_data")
        if not session_cart:
            return

        existing = StoreCart.objects.filter(user=self.user, product_id__in=session_cart.keys())
        existing_map = {str(item.product_id): item for item in existing}

        new_records = []
        for pid_str, qty in session_cart.items():
            pid_int = int(pid_str)

            if pid_str in existing_map:
                item = existing_map[pid_str]
                item.quantity += qty
                item.save()
                continue

            try:
                product = ProductModel.objects.get(id=pid_int, is_active=True)
            except ProductModel.DoesNotExist:
                continue

            new_records.append(StoreCart(user=self.user, product=product, quantity=qty))

        if new_records:
            StoreCart.objects.bulk_create(new_records)

        self.session["cart_data"] = {}
        self.session.modified = True

    @property
    def items(self):
        cart_items = []
        queryset = StoreCart.objects.filter(user=self.user).select_related("product")
        for item in queryset:
            product = item.product
            product.quantity = item.quantity
            cart_items.append(product)
        return cart_items

    def add(self, product_id, quantity=1):
        cart_item, created = StoreCart.objects.get_or_create(
            user=self.user, product_id=product_id, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove(self, product_id):
        item = StoreCart.objects.get(product_id=product_id, user=self.user)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    def get_total_cart_price(self):
        items = StoreCart.objects.filter(user=self.user).select_related("product")
        return sum(item.product.price * item.quantity for item in items if item.product.is_active)
