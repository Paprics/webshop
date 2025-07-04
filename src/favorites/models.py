from django.contrib.auth import get_user_model
from django.db import models

from store.models import ProductModel


# Create your models here.
class FavoriteModel(models.Model):
    class Meta:
        db_table = "favorite"
        verbose_name = "Обране"
        verbose_name_plural = "Обране"
        unique_together = ("customer", "product")

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} -> {self.product}"
