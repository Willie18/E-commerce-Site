from rest_framework.urlpatterns import format_suffix_patterns
from .views import AuthViewSet,AuthRootView
from rest_framework import routers

from django.urls import path



router=routers.SimpleRouter()
router.register('',AuthViewSet,basename="auth")

urlpatterns=[
    path("",AuthRootView)
]+router.urls


# urlpatterns = format_suffix_patterns(urlpatterns)