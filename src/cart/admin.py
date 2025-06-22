from django.contrib import admin

from cart import models


@admin.register(models.StoreCart)
class StoreCartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")


@admin.register(models.OrderModel)
class OrderModelAdmin(admin.ModelAdmin): ...


@admin.register(models.OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin): ...
