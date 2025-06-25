from django.shortcuts import get_object_or_404, render  # noqa F401
from django.views.generic import DetailView, ListView

from store import models
from store.models import CategoryModelMPTT, ProductModel

from . import mixins
from .search_engines import SearchSQLite


class ProductsListView(mixins.SearchFilterMixin, ListView):

    model = ProductModel
    context_object_name = "products"
    paginate_by = 5
    template_name = "product_list.html"
    search_engine_class = SearchSQLite

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_params"] = self.request.GET.copy()
        if "page" in context["query_params"]:
            del context["query_params"]["page"]
        return context


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
        slug = self.kwargs.get("slug_category")
        category = get_object_or_404(CategoryModelMPTT, slug=slug)
        categories = category.get_descendants(include_self=True)

        return ProductModel.objects.filter(category__in=categories, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(CategoryModelMPTT, slug=self.kwargs.get("slug_category"))
        return context
