from django.contrib import admin

from .models import CustomerUser, ProfileCustomer


class ProfileInline(admin.StackedInline):  # Табличный вариант — TabularInline
    model = ProfileCustomer
    can_delete = False
    verbose_name_plural = "Профиль"


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "email", "first_name", "last_name")
    inlines = [ProfileInline]


# TODO: delete it
@admin.register(ProfileCustomer)
class ProfileCustomerAdmin(admin.ModelAdmin):
    pass
