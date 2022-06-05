from rest_framework import viewsets
from rest_framework.filters import SearchFilter 
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from django_filters import rest_framework as filters

from .serializers import ProductSerializer
from .models import Product

#product filter class
class ProductFilter(filters.FilterSet):

    class Meta:
        model=Product
        fields={
            "price":["lt","gt"],
            "category__title":["exact"],
            "title":["icontains","iexact"],
            "label":["icontains","iexact"],
            "slug":["exact"],
            "tags__name":["icontains"],
            "ratings__rate":["lt","gt"],
            "ratings__count":["lt","gt"]
        }
        # ["category__title","min_price","max_price","title","label","slug","tags"]

class ProductViewSet(viewsets.ModelViewSet):

    """
    GET         retrieves a single product with the given id
    PATCH       partial updates a product
    DELETE      deletes the product

    """    
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[filters.DjangoFilterBackend,SearchFilter,]
    search_fields = ['=title','price']
    filterset_class=ProductFilter
    permission_classes_by_action={
                        "create":[IsAdminUser],
                        "update":[IsAdminUser],
                        "destroy":[IsAdminUser],
                        "list":[IsAuthenticated],
                        "retrieve":[IsAuthenticated],
                        "partial_update":[IsAdminUser]}

    #overide the methods to give per method docstring
    def create(self, request,*args, **kwargs):
        """
        ``POST`` Generates a request to create a Product in the inventory

        Request POST /api/v1/products/

        NOTE for the tags field- the payload should be a valid json list of strings separated by commas

         ie ["cpu","hp"]

        Response

        """
        return super(ProductViewSet,self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            ``GET`` lists all ``Products`` in the inventory accessible by a ``User``.

            **Example request**:

                GET  /api/v1/products/ HTTP/1.1

                filters [category__name,price__gt,price__lt,title,tags__name....]

                NOTE: all string filters are case sensitive

    """
        return super(ProductViewSet,self).list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        ``PATCH`` generates a request to Patch the product

        Request POST /api/v1/products/1    -update product with id 1
        """
        return super().partial_update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        ``GET`` generates a request to retrieve the product with the specified id

        Request GET /api/v1/products/1    -retrieves product with id 1

        Response

        Product object

        """

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        ``DELETE`` generates a request to purge the item identified with the given id

        Request DELETE /api/v1/products/1

        """
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        ``PUT`` generates a request to update the item identified with the given id

        Request PUT /api/v1/products/1
        
        """
        return super().update(request, *args, **kwargs)
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
             # action is not set return default permission_classes
             return [permission() for permission in self.permission_classes]
    
    # def filter_by_category(self,request,categories=[]):
    #     products_by_category=Product.objects.all().filter(category__in=categories)
    #     page=self.paginate_queryset(products_by_category)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(products_by_category, many=True)
    #     return Response(serializer.data)





        
# Create your views here.
# class ProductList(APIView):
#     """
#     List all products, or create a new product.
#     """

#     def get(self,request,format=None):
#         products=Product.objects.all()
#         serializer=ProductSerializer(products,many=True)
#         return Response(serializer.data)

#     def post(self,request,format=None):
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class ProductDetail(APIView):
#     """
#     Retrieve, update or delete a product/item instance.
#     """

#     def get_object(self,pk):
#         try:
#             product=Product.objects.get(pk=pk)
#             return product
#         except Product.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):
#         product=self.get_object(pk)
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self,request,pk,format=None):
#         product=self.get_object(pk)
#         serializer=ProductSerializer(instance=product,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk,format=None):
#         product=self.get_object(pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
# class CategoryView(APIView):
#     pass