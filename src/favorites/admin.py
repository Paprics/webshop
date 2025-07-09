from django.contrib import admin

from favorites.models import FavoriteModel


# Register your models here.
@admin.register(FavoriteModel)
class FavoriteAdmin(admin.ModelAdmin): ...
