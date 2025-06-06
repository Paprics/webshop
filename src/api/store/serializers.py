from rest_framework import serializers

from common.models import Content
from store.models import CategoryModel, CategoryModelMPTT


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"


class CategoryMPTTSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModelMPTT
        fields = ["id", "category_name", "slug", "is_active", "display_order", "parent", "children"]

    def get_children(self, obj):
        # obj.children — это QuerySet прямых детей, thanks related_name
        children_qs = obj.children.all()
        if children_qs.exists():
            return CategoryMPTTSerializer(children_qs, many=True).data
        return []


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "title", "slug", "content", "created_at", "updated_at"]


class ContentSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
