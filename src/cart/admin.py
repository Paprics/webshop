from django.contrib import admin

from cart import models


from django.contrib import admin
from . import models

class OrderItemInline(admin.TabularInline):
    model = models.OrderItemModel
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = False
    readonly_fields = ('product', 'quantity', 'price_at_order_time')

@admin.register(models.OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('get_order_info', "customer", "status", "is_paid")
    inlines = [OrderItemInline]
    readonly_fields = ('get_order_info', "customer", "status", "is_paid")
    fields = ('get_order_info', "customer", "status", "is_paid")  # 💥 Вот это добавь

    @admin.display(description='Замовлення')
    def get_order_info(self, obj):
        return f'Зам. №{obj.id} від {obj.created_at.strftime("%Y.%m.%d")} р.'



# # ORDER ITEMS
# @admin.register(models.OrderItemModel)
# class OrderItemModelAdmin(admin.ModelAdmin):...


# # STORE CART
# @admin.register(models.StoreCart)
# class StoreCartAdmin(admin.ModelAdmin):...