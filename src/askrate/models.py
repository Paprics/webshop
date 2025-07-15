from django.contrib.auth import get_user_model
from django.db import models

from store.models import ProductModel


class AskRateModel(models.Model):
    TYPE_CHOICES = [
        ("review", "Відгук"),
        ("question", "Питання"),
    ]

    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_askrates",
        blank=True,
        null=True,
        verbose_name="Клієнт",
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="product_askrates",
        verbose_name="Товар",
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    text = models.TextField(max_length=1000, verbose_name="Зміст")
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        blank=True,
        null=True,
        verbose_name="Рейтинг",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    answer = models.TextField(blank=True, null=True, verbose_name="Відповідь")
    answered_at = models.DateTimeField(blank=True, null=True, verbose_name="Дата відповіді")

    class Meta:
        db_table = "ask_rate"
        ordering = ["-created_at"]
        verbose_name = "Відгуки - Запитання"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()} — {self.customer or 'Гість'} — {self.product}"
