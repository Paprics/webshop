from rest_framework import serializers

from common.models import Content
from store.models import ProductModel

# class CategoryMPTTSerializer(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CategoryModelMPTT
#         fields = ["id", "category_name", "slug", "is_active", "display_order", "parent", "children"]
#
#     def get_children(self, obj):
#         # obj.children — это QuerySet прямых детей, thanks related_name
#         children_qs = obj.children.all()
#         if children_qs.exists():
#             return CategoryMPTTSerializer(children_qs, many=True).data
#         return []


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
