from django.contrib import admin

from .models import AskRateModel


@admin.register(AskRateModel)
class AskRateModelAdmin(admin.ModelAdmin):
    fields = ("product", "get_customer_username", "type", "text", "rating", "is_active", 'answer')
    readonly_fields = ("product", "get_customer_username", "type", "text", "rating")
    list_display = ("product", "get_customer_username", "text", 'is_active')
    list_filter = ("type", "created_at")
    list_editable = ('is_active',)
    search_help_text = "Пошук за текстом, товаром, ім’ям, email"
    search_fields = ("text", "product__title", "customer__first_name", "customer__last_name", "customer__email")
    search_lookup_allowed_fields = ("customer",)
    list_per_page = 20

    @admin.display(description="Користувач")
    def get_customer_username(self, obj):
        if not obj.customer:
            return "Гість"
        return obj.customer.get_full_name() or obj.customer.username

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
