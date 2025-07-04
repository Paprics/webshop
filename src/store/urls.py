from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("category/<slug:slug_category>/", views.ProductsListView.as_view(), name="products_category"),
    path("products/<slug:slug_product>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("search/", views.ProductsListView.as_view(), name="products_search"),
    path("create_category/", views.CreateCategoryView.as_view(), name="create_category"),
    path("create_products/", views.CreateProductsView.as_view(), name="create_product"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
