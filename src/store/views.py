from django.shortcuts import get_object_or_404, render  # noqa F401
from django.views.generic import DetailView, ListView

from store import models
from store.models import CategoryModelMPTT, ProductModel


class ProductSearchView(ListView):
    model = ProductModel
    paginate_by = 10
    context_object_name = "products"
    template_name = "product_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = ProductModel.objects.all()
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset


class ProductsListView(ListView):
    model = ProductModel
    context_object_name = "products"
    paginate_by = 5
    template_name = "product_list.html"

    def get_queryset(self):
        return models.ProductModel.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = models.ProductModel
    template_name = "product_detail.html"
    context_object_name = "product"

    # По умолчанию DetailView ищет объект по pk, чтобы искать по slug:
    slug_field = "slug"
    slug_url_kwarg = "slug_product"


class ProductsCategoryView(ListView):
    model = ProductModel
    paginate_by = 6
    template_name = "product_list_category.html"

    def get_queryset(self):
        # Ловим слаг категории из url, ключ должен совпадать с шаблоном и urls.py
        slug = self.kwargs.get("slug_category")

        # Получаем категорию по слагу, если нет — 404
        category = get_object_or_404(CategoryModelMPTT, slug=slug)

        # Берём все дочерние категории + сама категория (вложенность учитываем)
        categories = category.get_descendants(include_self=True)

        # Фильтруем продукты, чтобы были из этих категорий и активные
        return ProductModel.objects.filter(category__in=categories, is_active=True)

    def get_context_data(self, **kwargs):
        # В контекст кладём текущую категорию для удобства в шаблоне
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(CategoryModelMPTT, slug=self.kwargs.get("slug_category"))
        return context
