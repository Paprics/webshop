from rest_framework import serializers

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
