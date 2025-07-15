from django.contrib import admin
from django.utils.html import format_html

from common.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("get_customer_name", "title", "message", "colored_status")
    list_display_links = ("get_customer_name", "title", "message")
    list_filter = ("status",)
    search_fields = ("title", "message", "email", "user__first_name", "user__last_name")
    search_help_text = "Пошук за заголовком, змістом, email або іменем користувача"
    readonly_fields = ('user', 'title', 'message', 'email', "phone_number")

    Feedback.get_customer_name.short_description = "Клієнт"

    @admin.display(description="Статус")
    def colored_status(self, obj):
        color_map = {
            'unreviewed': 'gray',
            'in_progress': 'orange',
            'urgent': 'red',
            'resolved': 'green',
        }
        color = color_map.get(obj.status, 'black')
        label = obj.get_status_display()
        return format_html('<span style="color: {};"><b>{}</b></span>', color, label)

    actions = ['make_unreviewed', 'make_in_progress', 'make_urgent', 'make_resolved']

    def make_unreviewed(self, request, queryset):
        updated = queryset.update(status=Feedback.Status.UNREVIEWED)
        self.message_user(request, f"{updated} звернень позначено як 'Не розглянуто'.")
    make_unreviewed.short_description = "Встановити статус 'Не розглянуто'"

    def make_in_progress(self, request, queryset):
        updated = queryset.update(status=Feedback.Status.IN_PROGRESS)
        self.message_user(request, f"{updated} звернень позначено як 'У роботі'.")
    make_in_progress.short_description = "Встановити статус 'У роботі'"

    def make_urgent(self, request, queryset):
        updated = queryset.update(status=Feedback.Status.URGENT)
        self.message_user(request, f"{updated} звернень позначено як 'Потребує негайного вирішення'.")
    make_urgent.short_description = "Встановити статус 'Потребує негайного вирішення'"

    def make_resolved(self, request, queryset):
        updated = queryset.update(status=Feedback.Status.RESOLVED)
        self.message_user(request, f"{updated} звернень позначено як 'Вирішено'.")
    make_resolved.short_description = "Встановити статус 'Вирішено'"

    # 1. Убрать кнопки “Сберегти і додати” і “Сберегти і продовжити”
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context=extra_context)

    # 2. Запретить создавать новые записи
    def has_add_permission(self, request):
        return False  # запрещаем добавлять новые записи вручную

    # 3. Запретить удалять записи
    def has_delete_permission(self, request, obj=None):
        return False  # запрещаем удалять записи

