from django.urls import path,include,re_path
from .views import api_root
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import urls
# from .views import schema_view
from rest_framework.authtoken.views import obtain_auth_token


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view=get_schema_view(
    openapi.Info(
        title="Django Ecommerce Site API",
        default_version="v1",
        description="Test",
        license=openapi.License(name="BSD License")
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns=[
    path("",api_root,name="core-api"),
    path("categories/",include("category.urls"),name="category-list"),
    path("products/",include("product.urls"),name="product-list"),
    path("cart/",include("basket.urls"),name="orders"),
    path("auth/",include("tokens.urls"),name="jwt-tokens"),
    path("api-token-auth/",include("rest_framework.urls",namespace="restframework")),
    path("users/",include("users.urls")),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0),name="schema-json"),
    re_path(r'^swagger/$',schema_view.with_ui('swagger',cache_timeout=0),name="schema-swagger-ui"),
    re_path(r'^redoc/$',schema_view.with_ui('swagger',cache_timeout=0),name="schema-redoc")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns=format_suffix_patterns(urlpatterns=urlpatterns)


