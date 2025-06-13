from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices

from store.models import ProductModel


class OrderStatus(TextChoices):
    PENDING = "pending", "Очікує оплати"
    PAID = "paid", "Оплачено"
    PROCESSING = "processing", "Обробляється"
    SHIPPED = "shipped", "Відправлено"
    DELIVERED = "delivered", "Доставлено"
    CANCELLED = "cancelled", "Скасовано"


# Before order
class StoreCart(models.Model):
    class Meta:
        db_table = "store_cart"
        verbose_name = "Кошик покупця (не оформлений)"
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

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Замовлення #{self.id} користувача {self.customer} від {self.created_at.strftime('%Y-%m-%d')}"


class OrderItemModel(models.Model):
    class Meta:
        db_table = "order_item"
        verbose_name = "Товари у замовленні"
        verbose_name_plural = verbose_name

    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)
