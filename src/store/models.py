from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class CategoryModelMPTT(MPTTModel):

    class Meta:
        db_table = "category_MPTT"
        verbose_name = "1.1. КатегорииMPTT"
        verbose_name_plural = "1.1. КатегорииMPTT"
        ordering = ["display_order"]

    # FIX: Doesn't work
    class MPTTMeta:
        order_insertion_by = ["display_order"]
        db_table = "categoryMptt"
        verbose_name = "9. Категории MPTT"
        verbose_name_plural = "9. Категории MPTT"

    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def __str__(self):
        return self.category_name


class CategoryModel(models.Model):
    class Meta:
        db_table = "category"
        verbose_name = "Категорія"
        verbose_name_plural = "1. Категорії"
        ordering = ["display_order", "category_name"]

    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)

    # # self-referential foreign key
    # parent = models.ForeignKey(
    #     'self',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='children',
    #     verbose_name='Родительская категория',
    # )

    def __str__(self):
        return self.category_name


class ProductModel(models.Model):
    class Meta:
        db_table = "product"
        verbose_name = "2. Товар"
        verbose_name_plural = "2. Товари"

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    article = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="product/image/", blank=True)  # TODO -> M2O other model
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey("CategoryModel", on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class OrderModel(models.Model):
    class Meta:
        db_table = "order"
        verbose_name = "3. Замовлення"
        verbose_name_plural = "3. Замовлення"

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Замовлення #{self.id} користувача {self.customer} від {self.created.strftime('%Y-%m-%d')}"


class OrderItemModel(models.Model):
    class Meta:
        db_table = "order_item"
        verbose_name = "Позиція замовлення(hide)"
        verbose_name_plural = "Позиція замовлення(hide)"

    order = models.ForeignKey(OrderModel, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"


class FavoriteModel(models.Model):
    class Meta:
        db_table = "favorite"
        verbose_name = "Обране"
        verbose_name_plural = "Обране"
        unique_together = ("customer", "product")

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("ProductModel", on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} -> {self.product}"


# TODO: fix -> anonymous user???
class CommentModel(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "Коментарій"
        verbose_name_plural = "Коментарі"

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("ProductModel", on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} -> {self.product.title} | {self.is_active} |"
