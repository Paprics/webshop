from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import TextField
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class CategoryModelMPTT(MPTTModel):
    class Meta:
        db_table = "category_MPTT"
        verbose_name = "1. Категорії товарів"
        verbose_name_plural = verbose_name
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


class ProductModel(models.Model):
    class Meta:
        db_table = "product"
        verbose_name = "2. Товар"
        verbose_name_plural = "2. Товари"

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    article = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = TextField(blank=True, validators=[MaxLengthValidator(1000)])
    image = models.ImageField(upload_to="image/", blank=True)  # TODO -> M2O other model
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey("CategoryModelMPTT", on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


# TODO: fix -> anonymous user???
class CommentModel(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "Коментарій"
        verbose_name_plural = "Коментарі"

    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey("ProductModel", on_delete=models.CASCADE, default=1)
    text = models.TextField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer} -> {self.product.title} | {self.is_active} |"

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"slug": self.product.slug})
