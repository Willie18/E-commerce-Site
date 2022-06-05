from datetime import datetime
from rest_framework.decorators import action,api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ImproperlyConfigured


from product.models import Product

from .basket import Summary
from .serializers import BasketSerializer,AddBasketSerializer,EmptySerializer, OrderSerializer
from .serializers import BasketSerializer,DeleteItemBasketSerializer

from basket.models import Order, OrderItem

class CartView(viewsets.GenericViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Product.objects.all()
    serializer_class=EmptySerializer
    serializer_classes={
        "add_item_to_cart":AddBasketSerializer,
        "remove_item_from_cart":DeleteItemBasketSerializer,
        "update_cart_item":AddBasketSerializer
    }
    @action(methods=["post"],detail=False)
    def add_item_to_cart(self,request,format=None):
        """
        Adds the item specified by the {productid} to the cart 

        Request Payload {"productid:'' productqty:{''}}

        Note: this action adds the item to the cart with the quantity specified

        Response

        an updated cart object depicting the cart and the items in after adding the item in the cart 

        """
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket=Summary(request=request)
        product=self.queryset.filter(pk=serializer.data["productid"]).first()
        if product is None:
            return Response(data={"message":"Given Product ID Not Found"},status=status.HTTP_404_NOT_FOUND)
        basket.add(product,qty=serializer.data["productqty"])
        serializer=BasketSerializer(basket)
        return Response({"details":serializer.data})

    @action(methods=["post"],detail=False)
    def remove_item_from_cart(self,request):
        """        
        Pops an item quantity specified by the {product-id} from the cart 

        Request Payload {"productid:''}

        Note:this action reduces the {quantity} of the specified product by one

        if the product id passed is not in the cart the cart will remain unchanged

        Response

        an updated cart object depicting the cart and the items in remaining in the cart
            
        """
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket=Summary(request=request)
        basket.delete(**serializer.data)
        serializer=BasketSerializer(basket)
        return Response({"details":serializer.data})

    @action(methods=["PUT"],detail=False)
    def update_cart_item(self,request):
        """        
        Updates an item's quantity specified by the {product-id}

        Request Payload {"productid:'' productqty:""}

        Note:this action sets the {quantity} of the product to specified quantity

        if the product id passed is not in the cart the cart will remain unchanged

        Response

        an updated cart object depicting the cart and the items in remaining in the cart
            
        """
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket=Summary(request=request)
        basket.update(**serializer.data)
        serializer=BasketSerializer(basket)
        return Response({"details":serializer.data})
        
    @action(methods=["GET"],detail=False)
    def list_cart_items(self,request):
        """
        This view presents the items currently in cart

        No parameters

        Request GET  /api/v1/cart/list_cart_items

        Response

        {
    "items": {
        "transaction_id": "91d239fb-9da3-4526-b5f1-f78886686b19",
        "price": "250",
        "items": [
            {
                "qty": 5,
                "product": "juice",
                "product_id": "1",
                "price": 50,
                "total_price": 250
            }
        ],
        "ordered": false
    }
}
        """
        basket=Summary(request=request)
        basket.save()
        #return the response
        serializer=BasketSerializer(basket)
        return Response({"details":serializer.data})
    @action(methods=["post"],detail=False)
    def check_out(self,request):
        """
        This view check's out the cart session:

        No parameters

        Request POST /api/v1/cart/check_out/

        Response

        an updated cart object depicting items in the cart with the ordered attribute set to true

        """
        basket=Summary(request=request)
        #check if cart has items
        if not basket.basket["items"].items():
            return Response("cart has no items to add",status=status.HTTP_400_BAD_REQUEST)
        basket.save()
        basket.checkout()
        # order,created=Order.objects.update_or_create(
           
        # )
        order=Order(
             user=request.user,
            ref_code=basket.basket.get("id",None),
            checked_out=True,
            ordered_date=datetime.now()
        )
        order.save()        
        [OrderItem(
            product=Product.objects.filter(pk=id).first(),
            quantity=details["qty"],
            order=order
        ).save() for id,details in basket.basket["items"].items()]
        
        serializer=BasketSerializer(basket)
        return Response({"details":serializer.data})

    @action(methods=["get"],detail=False)
    def orders(self,request):

        """
        GET: list orders belonging to a user
    
        """
        orders=Order.objects.all().filter(user=request.user)
        context=[OrderSerializer(order).data for order in orders]
        return Response(context)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

@api_view()
def cartRootView(request):
    """
        This endpoint allows products to be added,updated and removed to/from the cart

        below are the actions the endpoint serves

    """    
    routes={
        "add-item-to-cart":f"{request.build_absolute_uri()}add_item_to_cart",
        "remove-item-from-cart":f"{request.build_absolute_uri()}remove_item_from_cart",
        "list-cart-items":f"{request.build_absolute_uri()}list_cart_items"
    }
    return Response(data=routes,status=status.HTTP_202_ACCEPTED)