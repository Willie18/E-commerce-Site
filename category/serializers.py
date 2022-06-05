from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Category
        fields=["title","description","id"]
        # ref_name="category_serializer"