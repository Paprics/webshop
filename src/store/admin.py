from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from store.forms import ProductAdminForm
from store.models import CategoryModelMPTT, CommentModel, ProductModel


@admin.register(CategoryModelMPTT)
class StoreMPTTAdmin(DraggableMPTTAdmin):
    class MPTTMeta:
        order_insertion_by = ["category_name"]

    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("category_name",)}
    list_filter = (("parent", TreeRelatedFieldListFilter),)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "price", "article", "quantity", "is_active", "category")


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin): ...
