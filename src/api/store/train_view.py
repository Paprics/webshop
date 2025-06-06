from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.store import serializers
from store.models import ProductModel


class ListProductAPI(APIView):
    "Список всіх товарів з БД (APIView)"

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ProductSerializer
    queryset = ProductModel.objects.all()

    # From paginator
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10

        products = ProductModel.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # without pagination
    # def get(self, request):
    #     products = ProductModel.objects.all()
    #     serializer = serializers.ProductSerializer(products, many=True)
    #     return Response(serializer.data)


class DetailProductAPI(APIView):
    "Товар по slug: (APIView)"

    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ProductSerializer
    queryset = ProductModel.objects.all()

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        product = get_object_or_404(self.queryset, slug=slug)
        serializer = self.serializer_class(product)
        return Response(serializer.data)

    # This POST method on this endpoint doesn't look good.
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)  #
        serializer.save()
        return Response(serializer.data)

    def get_object(self):
        slug = self.kwargs.get("slug")  # parameter from URL
        return get_object_or_404(self.queryset, slug=slug)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()  # get the existing object to update
        data = request.data
        serializer = self.serializer_class(
            instance, data=data, partial=True
        )  # partial=True for partial update, updating only some fields
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()  # get existing object to update fully
        data = request.data
        serializer = self.serializer_class(instance, data=data)  # full update, all fields required
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
