from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path("products/", views.ProductsListView.as_view(), name="products_list"),
    path("products/<slug:slug_product>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("category/<slug:slug_category>/", views.ProductsCategoryView.as_view(), name="products_category")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
