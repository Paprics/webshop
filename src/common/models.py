from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


# Create your models here.
class Content(models.Model):
    class Meta:
        db_table = "Content_site"
        verbose_name = "Сторінки"
        verbose_name_plural = verbose_name

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content_detail", kwargs={"slug": self.slug})


class Feedback(models.Model):
    class Status(models.TextChoices):
        UNREVIEWED = "unreviewed", "Не розглянуто"
        IN_PROGRESS = "in_progress", "У роботі"
        URGENT = "urgent", "Потребує негайного вирішення"
        RESOLVED = "resolved", "Вирішено"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedbacks")
    title = models.CharField(max_length=255)
    message = models.TextField(max_length=1500)

    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.UNREVIEWED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Feedback"
        verbose_name = "Зворотній зв'язок"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title} — {self.get_status_display()}"
