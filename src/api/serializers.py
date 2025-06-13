from rest_framework import serializers

from accounts.models import CustomerUser
from common.models import Content
from store.models import CategoryModelMPTT, ProductModel


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ("id", "phone_number", "first_name", "last_name", "email")


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = CategoryModelMPTT
        fields = ("id", "category_name", "slug", "is_active", "display_order", "children")

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True, context=self.context).data
        return []


class CategorySerializerBase(serializers.ModelSerializer):
    class Meta:
        model = CategoryModelMPTT
        fields = "__all__"
