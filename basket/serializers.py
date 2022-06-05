from tkinter.tix import Tree
from rest_framework import serializers

from basket.models import Order, OrderItem
from product.models import Product
from product.serializers import ProductSerializer


class BasketSerializer(serializers.Serializer):
    transaction_id=serializers.CharField()
    price=serializers.CharField()
    items=serializers.ListField()
    ordered=serializers.BooleanField(default=False)
    
class AddBasketSerializer(serializers.Serializer):
    productid=serializers.IntegerField()
    productqty=serializers.IntegerField(default=1)

class DeleteItemBasketSerializer(serializers.Serializer):
    productid=serializers.CharField()

class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name="List cart items"
    pass

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["title","price"]

class OrderItemSerializer(serializers.ModelSerializer):
    product=ItemSerializer()
    class Meta:
        model=OrderItem
        fields=["product","quantity"]

class OrderSerializer(serializers.ModelSerializer):
    # ref_code=serializers.CharField(max_length=100)
    # total_price=serializers.FloatField()
    # creation_date=serializers.DateTimeField()
    # checked_out=serializers.BooleanField()
    # ordered_date=serializers.DateField()
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=["ref_code","total_price","creation_date","checked_out","ordered_date","items"]