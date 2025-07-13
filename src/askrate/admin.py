from django.contrib import admin

from .models import AskRateModel


@admin.register(AskRateModel)
class AskRateModelAdmin(admin.ModelAdmin):
    list_display = ("product", "get_customer_username", "text")
    list_filter = ("type", "created_at")
    search_help_text = "Пошук за текстом, товаром, ім’ям, email"
    search_fields = ("text", "product__title", "customer__first_name", "customer__last_name", "customer__email")
    search_lookup_allowed_fields = ("customer",)
    list_per_page = 20

    @admin.display(description="Користувач")
    def get_customer_username(self, obj):
        if not obj.customer:
            return "Гість"
        return obj.customer.get_full_name() or obj.customer.username

    # fieldsets = (
    #     (None, {'fields': ('type', 'product', 'customer', 'text', 'rating')}),
    #     ('Адміністрування', {'fields': ('is_active', 'answer', 'answered_at')}),
    #     ('Системна інформація', {'fields': ('created_at', 'updated_at')}),
    # )
