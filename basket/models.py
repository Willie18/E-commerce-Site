from django.db import models
from users.models import CustomerUser
from product.models import Product
# Create your models here.


#after checkout add the items to the model
class Order(models.Model):
    user=models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name="orders")
    ref_code=models.CharField(max_length=100,unique=True)
    creation_date=models.DateTimeField(auto_now_add=True, verbose_name="creation date")
    checked_out=models.BooleanField(default=False,verbose_name="checked out")
    ordered_date=models.DateField(verbose_name="ordered date",null=True)
    def __str__(self) -> str:
        return self.ref_code
    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items",null=True)

    def total_price(self):
        return self.product.price * self.quantity
    def price(self):
        return self.product.price
    
    def __str__(self) -> str:
        return self.product.title