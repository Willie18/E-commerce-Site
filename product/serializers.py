from rest_framework  import serializers
from .models import Product,ProductRating
from category.serializers import CategorySerializer


from drf_writable_nested.serializers import WritableNestedModelSerializer

from taggit.serializers import (TaggitSerializer,TagListSerializerField)

from .models import PRODUCT_LABEL


class ProductRatingSerializer(serializers.HyperlinkedModelSerializer):
    count=serializers.IntegerField()
    rate=serializers.FloatField()
    class Meta:
        model=ProductRating
        fields=["rate","count"]

class ProductSerializer(TaggitSerializer,WritableNestedModelSerializer,serializers.HyperlinkedModelSerializer):
    # id=serializers.IntegerField(read_only=True)
    # title=serializers.CharField(required=False, allow_blank=True, max_length=100)
    # description=serializers.CharField()
    # price=serializers.DecimalField(decimal_places=0,max_digits=6)
    label=serializers.ChoiceField(PRODUCT_LABEL,required=True)
    # image=serializers.ImageField(allow_empty_file=True)
    # thumbnail=serializers.ImageField(allow_empty_file=True)
    # created=serializers.DateField()
    category=CategorySerializer()
    tags=TagListSerializerField()
    ratings=ProductRatingSerializer()
    # slug=serializers.SlugField(allow_blank=True)

    class Meta:
        model=Product
        fields=["id","title","description","price","label","category","created","get_image","get_thumbnail","tags","get_absolute_url","slug","ratings"]

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Product` instance, given the validated data.
    #     """
       
    #     return Product.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Product` instance, given the validated data.
    #     """
    #     #update nested i.e tags and category

    #     if "category" in validated_data:
    #         nested_serializer=self.fields["category"]
    #         nested_instance=instance.category
    #         nested_data=validated_data.pop("category")

    #         #Runs the update on category serializer the nested data belongs to

    #         nested_serializer.update(nested_instance,nested_data)
        
    #     if "tags" in validated_data:
    #         nested_serializer=self.fields["tags"]
    #         nested_instance=instance.tags
            # nested_data=validated_data.pop("tags")

            #Runs the update on category serializer the nested data belongs to

            # print(dir(nested_serializer))

            # nested_serializer.update(nested_instance,nested_data)

        # super(ProductSerializer,self).update(instance=instance,validated_data=validated_data)

        # instance.title=validated_data.get("title",instance.title)
        # instance.description=validated_data.get("description",instance.description)
        # instance.price=validated_data.get("price",instance.price)
        # instance.label=validated_data.get("label",instance.label)
        # instance.image=validated_data.get("image",instance.image)
        # instance.thumbnail=validated_data.get("thumbnail",instance.thumbnail)
        # instance.created=validated_data.get("created",instance.created)
        # instance.slug=validated_data.get("slug",instance.slug)
        # instance.tags=validated_data.get("tags",instance.tags)
        # instance.save()
        # return instance