from django.urls import path

from rest_framework import routers

from .views import CartView,cartRootView

app_name = 'basket'

router=routers.SimpleRouter()
router.register("",CartView,basename="cart")


urlpatterns=[
    path("",cartRootView),
]+router.urls


# urlpatterns = [
#     path('', views.basket_summary, name='basket_summary'),
#     path('add/', views.basket_add, name='add-to-cart'),
#     path('delete/', views.basket_delete, name='remove-from-cart'),
#     path('update/', views.basket_update, name='basket_update'),
# ]