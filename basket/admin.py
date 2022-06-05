from django.contrib import admin

from basket.models import Order, OrderItem

# Register your models here.


class OrderAdminConfig(admin.ModelAdmin):
    list_display=["ref_code","user","creation_date","checked_out","ordered_date"]

class OrderItemAdminConfig(admin.ModelAdmin):
    list_display=["__str__","quantity","price","total_price"]

admin.site.register(OrderItem,OrderItemAdminConfig)
admin.site.register(Order,OrderAdminConfig)
