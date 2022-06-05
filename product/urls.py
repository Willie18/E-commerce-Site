from django.urls import path,include
from rest_framework import routers
from .views import ProductViewSet


router=routers.SimpleRouter()
router.register(r"",ProductViewSet)


urlpatterns=[
    # path("",ProductList.as_view()),
    # path("<int:pk>/",ProductDetail.as_view())
    path("",include(router.urls))
]