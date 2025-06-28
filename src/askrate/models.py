from django.contrib.auth import get_user_model
from django.db import models
from store.models import ProductModel


class AskRateModel(models.Model):
    TYPE_CHOICES = [
        ('review', 'Відгук'),
        ('question', 'Питання'),
    ]

    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_askrates',
        blank=True,
        null=True
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name='product_askrates'
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    text = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    answer = models.TextField(blank=True, null=True)
    answered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ask_rate'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.get_type_display()} — {self.customer or 'Анонім'} — {self.product}"



