from rest_framework import generics, permissions
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination

from common.models import Content
from store.models import CategoryModelMPTT, ProductModel

from . import serializers


class ContentPagination(PageNumberPagination):
    page_size = 12


class ContentListView(ListCreateAPIView):
    "Список всіх статей сайту"

    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer
    pagination_class = ContentPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    "Сторінки сайту (контент) по slug"

    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProductListView(ListCreateAPIView):
    "Список всіх товарів"

    queryset = ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    "Товар по slug"

    queryset = ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class ProductByCategoryView(ListAPIView):
    "Список всіх товарів в категорії"

    serializer_class = serializers.ProductSerializer
    pagination_class = ContentPagination

    def get_queryset(self):
        slug = self.kwargs.get("slug_category")

        category = CategoryModelMPTT.objects.filter(slug=slug, is_active=True).first()
        if not category:
            return ProductModel.objects.none()

        return ProductModel.objects.filter(category=category, is_active=True).order_by("title")


class CategoryListView(ListCreateAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return (
            CategoryModelMPTT.objects.filter(parent=None, is_active=True)
            .prefetch_related("children")
            .order_by("display_order")
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryModelMPTT.objects.all()
    serializer_class = serializers.CategorySerializerBase
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]
