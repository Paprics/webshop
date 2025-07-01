from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404, render  # noqa F401
from django.views.generic import DetailView, ListView, TemplateView

from askrate.models import AskRateModel
from store import models
from store.models import CategoryModelMPTT, ProductModel

from . import mixins, utils
from .search_engines import SQLiteSearchEngine


class ProductsListView(mixins.SearchFilterMixin, mixins.FavoriteAnnotateMixin, ListView):

    model = ProductModel
    context_object_name = "products"
    paginate_by = 5
    template_name = "product_list.html"
    search_engine_class = SQLiteSearchEngine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_params"] = self.request.GET.copy()
        if "page" in context["query_params"]:
            del context["query_params"]["page"]
        return context


class ProductDetailView(mixins.FavoriteAnnotateMixin, DetailView):
    model = models.ProductModel
    template_name = "product_detail.html"
    context_object_name = "product"

    # По умолчанию DetailView ищет объект по pk, чтобы искать по slug:
    slug_field = "slug"
    slug_url_kwarg = "slug_product"

    # def get_queryset(self):
    #     return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.object — текущий продукт, по которому DetailView сделал запрос
        context["reviews"] = AskRateModel.objects.filter(is_active=True, product=self.object, type="review")[:10]
        context["questions"] = AskRateModel.objects.filter(is_active=True, product=self.object, type="question")[:10]

        context["recommendations"] = (
            models.ProductModel.objects.exclude(id=self.object.id)
            .annotate(
                same_category=Case(
                    When(category=self.object.category, then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .order_by("-same_category")[:4]
        )

        return context


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


class CreateCategoryView(TemplateView):
    template_name = "create.html"

    def get(self, request, *args, **kwargs):
        utils.create_categories()
        return super().get(request, *args, **kwargs)


class CreateProductsView(TemplateView):
    template_name = "create.html"

    def get(self, request, *args, **kwargs):
        utils.create_products()
        return super().get(request, *args, **kwargs)
