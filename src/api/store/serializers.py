from rest_framework import serializers
from store.models import CategoryModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'