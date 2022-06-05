from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.http import Http404
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from .serializers import CategorySerializer
from .models import Category

from django_filters import rest_framework as filters

# Create your views here.

class CategoryFilter(filters.FilterSet):
    class Meta:
        model=Category
        fields=["title",]

#viewset for creating, listing, retrieving, updating and deleting categories
class CategoryViewSet(viewsets.ModelViewSet):
    """
    GET: Retrieve a list of categories
    POST: Create a category
    PUT: Update a category
    PATCH: Patch a category
    DELETE: Delete a category    
    """
    serializer_class =CategorySerializer
    queryset=Category.objects.all().order_by("title")
    filterset_class=CategoryFilter
    permission_classes_by_action={
                        "create":[IsAdminUser],
                        "update":[IsAdminUser],
                        "destroy":[IsAdminUser],
                        "list":[IsAuthenticated],
                        "retrieve":[IsAuthenticated],
                        "partial_update":[IsAdminUser]}

    def retrieve(self, request, *args, **kwargs):
        """
        ``GET`` generates a request to retrieve the Category with the specified id

        Request GET /api/v1/categories/1    -retrieves category with id 1

        Response

        Category object
        """
        return super().retrieve(request, *args, **kwargs)
    def partial_update(self, request, *args, **kwargs):
        """
        ``PATCH`` generates a request to Patch the Category

        Request POST /api/v1/categories/1    -update Category with id 1
        
        """
        return super().partial_update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        """
        ``DELETE`` generates a request to purge the Category identified with the given id

        Request DELETE /api/v1/categories/1

        """
        return super().destroy(request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        """
        ``POST`` Generates a request to create a category

        Request POST /api/v1/categories/
        
        Payload   {
            "title":       "monitors",
            "description": "28" monitors"
        }

        Response

        page of categories including the newly created one


        """
        return super().create(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        """
        ``GET`` retrieves a list of categories

        A list of all the categories

        Request GET api/v1/categories

        """
        return super().list(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        """

        ``PUT`` generates a request to update the category

        Request PUT api/v1/categories/1

        """
        return super().update(request, *args, **kwargs)
    
    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
             # action is not set return default permission_classes
             return [permission() for permission in self.permission_classes]

# class CategoryDetail(Serializer.):
#     """
#         Retrieve, update or delete a single category instance.
#     """
#     def get_object(self,pk):
#         try:
#             category=Category.objects.get(pk=pk)
#             return category
#         except category.DoesNotExist:
#             raise Http404

#     def put(self,request,pk,format=None):
#         category=self.get_object(pk=pk)
#         serializer=CategorySerializer(instance=category,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk,format=None):
#         category=self.get_object(pk=pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def get(self,request,pk,format=None):
#         category=self.get_object(pk=pk)
#         serializer=CategorySerializer(category)
#         return Response(serializer.data)



