from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (GenericAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api import serializers
from api.serializers import ContentSerializer
from common.models import Content
from store.models import ProductModel


class ContentListCreateView(ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_field = "slug"


class ProductDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(["GET"])
@permission_classes([AllowAny])
def test_api(request):
    return Response({"message": "API is working"})
