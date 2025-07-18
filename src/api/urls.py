from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views

app_name = "api"


schema_view = get_schema_view(
    openapi.Info(
        title="Site API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("auth/", include("djoser.urls.jwt")),
    #
    path("customer/", views.CustomerListCreateView.as_view(), name="customer-list"),
    path("customer/<int:pk>/", views.CustomerDetailView.as_view(), name="customer-detail"),
    #
    path("products/", views.ProductListView.as_view(), name="products_list"),
    path(
        "products/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/category/<slug:slug_category>/",
        views.ProductByCategoryView.as_view(),
        name="products_by_category",
    ),
    #
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "category/<slug:slug>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
]
