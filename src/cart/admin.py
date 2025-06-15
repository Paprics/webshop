from django.contrib import admin

from cart import models


@admin.register(models.StoreCart)
class StoreCartAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")
