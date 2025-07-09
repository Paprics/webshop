from django.contrib import admin

from cart import models


@admin.register(models.StoreCart)
class StoreCartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")


@admin.register(models.OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "is_paid", "customer")


@admin.register(models.OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ("product__title", "order")
