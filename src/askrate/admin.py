from django.contrib import admin
from .models import AskRateModel

# Register your models here.
@admin.register(AskRateModel)
class AskRateModel(admin.ModelAdmin):...