from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from store.models import (CategoryModel, CategoryModelMPTT, CommentModel,
                          FavoriteModel, OrderItemModel, OrderModel,
                          ProductModel)

# Register your models here.


@admin.register(CategoryModel)
class StoreAdmin(admin.ModelAdmin): ...


@admin.register(CategoryModelMPTT)
class StoreMPTTAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("category_name",)}


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin): ...


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin): ...


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin): ...


@admin.register(FavoriteModel)
class FavoriteAdmin(admin.ModelAdmin): ...


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin): ...
