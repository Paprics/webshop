from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class CategoryModelMPTT(MPTTModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "category_MPTT"
        verbose_name = "2. Категорії товарів"
        verbose_name_plural = "2. Категорії товарів"
        ordering = ["display_order"]

    class MPTTMeta:
        order_insertion_by = ["display_order"]


class ProductModel(models.Model):
    class Meta:
        db_table = "product"
        verbose_name = "1. Товар"
        verbose_name_plural = "1. Товари"

    title = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(max_length=100, blank=True)
    article = models.CharField(max_length=10, unique=True, verbose_name="Артикуль")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    description = TextField(
        blank=True, validators=[MaxLengthValidator(1000)], verbose_name="Опис"
    )
    image = models.ImageField(
        upload_to="image/", blank=True, verbose_name="Зображення"
    )  # TODO -> M2O other model
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кіл-ть")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    category = models.ForeignKey(
        "CategoryModelMPTT", on_delete=models.PROTECT, verbose_name="Категорія"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
