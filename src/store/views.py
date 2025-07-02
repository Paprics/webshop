from django.db.models import (BooleanField, Case, Exists, IntegerField,
                              OuterRef, Value, When)
from django.shortcuts import get_object_or_404, render  # noqa F401
from django.views.generic import DetailView, ListView, TemplateView

from askrate.models import AskRateModel
from favorites.models import FavoriteModel
from store import models
from store.models import CategoryModelMPTT, ProductModel

from . import mixins, utils
from .search_engines import SQLiteSearchEngine


class ProductsListView(mixins.SearchFilterMixin, mixins.FavoriteAnnotateMixin, ListView):
    model = ProductModel
    context_object_name = "products"
    paginate_by = 9
    template_name = "product_list.html"
    search_engine_class = SQLiteSearchEngine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_params"] = self.request.GET.copy()
        if "page" in context["query_params"]:
            del context["query_params"]["page"]
        return context

    def get_queryset(self):
        slug = self.kwargs.get("slug_category")
        user = self.request.user

        base_qs = ProductModel.objects.filter(is_active=True)
        if slug:
            category = get_object_or_404(CategoryModelMPTT, slug=slug)
            categories = category.get_descendants(include_self=True)
            base_qs = base_qs.filter(category__in=categories)

        if user.is_authenticated:
            favorites_subquery = FavoriteModel.objects.filter(customer=user, product=OuterRef("pk"))
            base_qs = base_qs.annotate(is_favorite=Exists(favorites_subquery))
        else:
            base_qs = base_qs.annotate(is_favorite=Value(False, output_field=BooleanField()))

        return base_qs


class ProductDetailView(mixins.FavoriteAnnotateMixin, DetailView):
    model = models.ProductModel
    template_name = "product_detail.html"
    context_object_name = "product"

    # По умолчанию DetailView ищет объект по pk, чтобы искать по slug:
    slug_field = "slug"
    slug_url_kwarg = "slug_product"

    def get_queryset(self):
        return super().get_queryset()

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
