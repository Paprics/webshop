from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.store import serializers
from api.store.serializers import ContentSerializer
from common.models import Content
from store import models


class CategoriesViewApi(viewsets.ModelViewSet):
    """Категорії товарів | Product category"""

    permission_classes = [AllowAny]
    queryset = models.CategoryModel.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class CategoriesMPTTViewApi(viewsets.ModelViewSet):
    "Вкладененні катерегії товарів | Nested category"

    queryset = models.CategoryModelMPTT.objects.filter(is_active=True, parent__isnull=True)  # only parent
    serializer_class = serializers.CategoryMPTTSerializer


class ContentViewApiRetrieve(generics.RetrieveAPIView):
    "Сторінки сайту (static) | Site pages"

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "pk"  # fild for search qs

    def get_queryset(self):
        return Content.objects.filter(is_published=True)


class ContentViewApiList(generics.ListAPIView):
    "Список сторінок сайту | List of site pages"

    queryset = Content.objects.filter(is_published=True)
    serializer_class = serializers.ContentSerializerList


class ContentViewApiCreate:
    """Створення контенту | Create content"""

    pass


class ContentViewApiUpdate: ...


class ContentViewApiPartial: ...


class ContentViewApiDelete: ...


@api_view(["GET"])
@permission_classes([AllowAny])
def test_api(request):
    return Response({"message": "API is working"})
