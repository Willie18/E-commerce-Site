from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
# from rest_framework_swagger.views import get_swagger_view

# Create your views here.

# schema_view=get_swagger_view(title="Django Ecommerce Site")

@api_view(["GET"])
def api_root(request,format=None):
    """
    ``GET`` List all the endpoints exposed in this app

    Request api/v1/

    Response an object of all the endpoints exposed
    """
    return Response({
        "categories":reverse("category-list",request=request,format=format),
        "products":reverse("product-list",request=request,format=format),
        "orders":f"{request.build_absolute_uri()}cart",
        "tokens":f"{request.build_absolute_uri()}auth",
        "users":f"{request.build_absolute_uri()}auth",
})

