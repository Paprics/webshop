from django.contrib import admin

from common.models import Content, Feedback


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "short_content")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="Content")
    def short_content(self, obj):
        return (obj.content[:150] + "...") if len(obj.content) > 50 else obj.content


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "message", "status")
