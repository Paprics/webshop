from django.db import models
from django.urls import reverse


# Create your models here.
class Content(models.Model):
    class Meta:
        db_table = "content"
        verbose_name = "Контент"
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
