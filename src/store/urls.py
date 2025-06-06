from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import ProductDetailView

urlpatterns = [
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
