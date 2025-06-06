from django.shortcuts import render  # noqa F401
from django.views.generic import DetailView

from store import models


class ProductDetailView(DetailView):
    model = models.ProductModel
    template_name = "product_detail.html"
    context_object_name = "product"  # в шаблоне будет переменная media

    # По умолчанию DetailView ищет объект по pk, чтобы искать по slug:
    slug_field = "slug"
    slug_url_kwarg = "slug"
