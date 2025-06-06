from django.urls import path
from rest_framework.routers import DefaultRouter

from api.store import views

app_name = "api_store"

# for ViewSet(CRUD) class
router = DefaultRouter()
# router.register(r"categories", views.CategoriesViewApi, basename="categories")
# router.register(r"categories_nested", views.CategoriesMPTTViewApi, basename="categories_nested")

urlpatterns = router.urls + [
    path("test/", views.test_api),
    path("product/", views.ProductListCreateView.as_view(), name="product-list"),
    path("product/<slug:slug>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("content/", views.ContentListCreateView.as_view(), name="content-list-create"),
    path("content/<slug:slug>/", views.ContentDetailView.as_view(), name="content-detail"),
]
