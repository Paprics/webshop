from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.store import serializers
from store import models

class CategoriesViewApi(viewsets.ModelViewSet):
    "Категорії товарів | Product category"
    queryset = models.CategoryModel.objects.all()
    serializer_class = serializers.CategorySerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    return Response({"message": "API is working"})

