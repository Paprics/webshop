from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from store.models import (CategoryModel, CategoryModelMPTT, CommentModel,
                          FavoriteModel, OrderItemModel, OrderModel,
                          ProductModel)

# Register your models here.


@admin.register(CategoryModel)
class StoreAdmin(admin.ModelAdmin): ...


@admin.register(CategoryModelMPTT)
class StoreMPTTAdmin(DraggableMPTTAdmin):
    class MPTTMeta:
        order_insertion_by = ["category_name"]

    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("category_name",)}
    list_filter = (("parent", TreeRelatedFieldListFilter),)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "price", "article", "quantity", "is_active", "category")


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin): ...


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin): ...


@admin.register(FavoriteModel)
class FavoriteAdmin(admin.ModelAdmin): ...


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin): ...
