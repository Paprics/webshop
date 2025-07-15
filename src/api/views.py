from rest_framework import generics, permissions
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import PageNumberPagination

from accounts.models import CustomerUser
from store.models import CategoryModelMPTT, ProductModel

from . import serializers


class ContentPagination(PageNumberPagination):
    page_size = 12


class CustomerListCreateView(generics.ListCreateAPIView):
    "Список всіх Customers + Додавання нового Customer"

    queryset = CustomerUser.objects.all()
    serializer_class = serializers.CustomerUserSerializer
    pagination_class = ContentPagination

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return super().get_permissions()


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """"""

    queryset = CustomerUser.objects.all()
    serializer_class = serializers.CustomerUserSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


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

        return ProductModel.objects.filter(category=category, is_active=True).order_by(
            "title"
        )


class CategoryListView(ListCreateAPIView):
    "Список всіх катерій"

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
    "Редагування категорії"

    queryset = CategoryModelMPTT.objects.all()
    serializer_class = serializers.CategorySerializerBase
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]
