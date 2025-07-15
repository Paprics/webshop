from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Feedback(models.Model):
    class Status(models.TextChoices):
        UNREVIEWED = "unreviewed", "Не розглянуто"
        IN_PROGRESS = "in_progress", "У роботі"
        URGENT = "urgent", "Потребує негайного вирішення"
        RESOLVED = "resolved", "Вирішено"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedbacks",
        verbose_name="Користувач",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    message = models.TextField(max_length=1500, verbose_name="Зміст")

    email = models.EmailField(verbose_name="EMAIL")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер мобільного")

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.UNREVIEWED,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата звернення")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Feedback"
        verbose_name = "Зворотній зв'язок"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title} — {self.get_status_display()}"

    def get_customer_name(self):
        return "Гість" if self.user is None else f"{self.user.first_name} {self.user.last_name}"
