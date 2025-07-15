from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices

from store.models import ProductModel


class OrderStatus(TextChoices):
    PROCESSING = "processing", "Обробляється"
    SHIPPED = "shipped", "Відправлено"
    DELIVERED = "delivered", "Доставлено"
    CANCELLED = "cancelled", "Скасовано"


# Before order
class StoreCart(models.Model):
    class Meta:
        db_table = "store_cart"
        verbose_name = "3. Кошик покупця"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


class OrderModel(models.Model):
    class Meta:
        db_table = "order"
        verbose_name = "Замовлення"
        verbose_name_plural = verbose_name

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Покупець')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата замавлевлення')
    is_paid = models.BooleanField(default=False, verbose_name='Сплачено')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PROCESSING, verbose_name='Статус')

    def __str__(self):
        return f"Замовлення #{self.id} користувача {self.customer} від {self.created_at.strftime('%Y-%m-%d')}"


class OrderItemModel(models.Model):
    class Meta:
        db_table = "order_item"
        verbose_name = "2. (Товари у замовленні)"
        verbose_name_plural = verbose_name

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} — {self.quantity} шт."
