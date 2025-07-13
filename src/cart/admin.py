from django.contrib import admin

from cart import models


# Замовлення
@admin.register(models.OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "is_paid", "customer")


# Позиції в замовленні
@admin.register(models.OrderItemModel)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ("product__title", "order")


# Кошик покупця
@admin.register(models.StoreCart)
class StoreCartAdmin(admin.ModelAdmin):
    list_display = ("get_user_full_name", "product", "quantity", "added_at")
    list_filter = ("user",)

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    get_user_full_name.short_description = "Покупець"
