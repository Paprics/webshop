from django.contrib import admin

from store.models import (CategoryModel, CategoryModelMPTT, CommentModel,
                          FavoriteModel, OrderItemModel, OrderModel,
                          ProductModel)

# Register your models here.


@admin.register(CategoryModel)
class StoreAdmin(admin.ModelAdmin): ...


@admin.register(CategoryModelMPTT)
class StoreMPTTAdmin(admin.ModelAdmin): ...


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
