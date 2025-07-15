from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from store.forms import ProductAdminForm
from store.models import CategoryModelMPTT, ProductModel


class ProductInline(admin.TabularInline):
    model = ProductModel
    extra = 0
    fields = ("title", "price", "article", "quantity", "is_active")
    show_change_link = True
    can_delete = False  # запретить удаление
    max_num = 0  # запретить добавление новых


@admin.register(CategoryModelMPTT)
class StoreMPTTAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("category_name",)}
    list_filter = (("parent", TreeRelatedFieldListFilter),)
    inlines = [ProductInline]


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "title",
        "price",
        "article",
        "quantity",
        "is_active",
        "category",
        "get_image",
    )
    search_fields = ("title", "article", "description", "category__category_name")
    list_filter = ("category", "is_active")

    @admin.display(description="Зображення")
    def get_image(self, obj):
        if obj.image:
            url = obj.image.url
        else:
            url = static("img/No_image.png")
        return format_html(
            '<img src="{}" width="60" height="60" style="object-fit:contain; border:1px solid #ccc;" />',
            url,
        )
