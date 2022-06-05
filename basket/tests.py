from urllib import response
from django.test import TestCase

import random
import time
from string import ascii_letters

from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.test import APIRequestFactory
from rest_framework import status
from basket.views import CartView

from product.models import Product
from category.models import Category

from .basket import Summary
from django.contrib.auth import get_user_model

from model_bakery import baker


random.seed(int(time.time()))


# Create your tests here.
class BasketTest(TestCase):
    def create_user(self):
        db=get_user_model()
        user=db.objects.create_user(
            "test@superuser.com","testsuperuser","password"
        )
        return user
    def create_Basket(self,request):
        request.user=self.create_user()
        self.client.login(email="test@superuser.com",password="password")
        request.session=self.client.session
        basket=Summary(request=request)
        return basket
    def create_product(self):
        product=Product()
        product.title="".join([random.choice(ascii_letters) for i in range(10)])
        product.description="".join([random.choice(ascii_letters) for i in range(100)])
        category=Category()
        category.title=title="".join([random.choice(ascii_letters) for i in range(10)])
        category.description=title="".join([random.choice(ascii_letters) for i in range(100)])
        category.save()
        product.category=category
        product.price=random.randint(1,1000)
        product.save()        
        return product
    def test_basket_creation(self):
        request=self.client.get("/api/v1/cart/list_cart_items")
        basket=self.create_Basket(request=request)
        self.assertTrue(isinstance(basket,Summary))
        self.assertIsNotNone(basket.basket)
        self.assertIsNotNone(basket.basket.get("id"))
    def test_basket_add(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        runs=random.randint(1,10)
        for run in range(runs):
            product=self.create_product()
            qty=random.randint(1,50)
            ## add product 1
            basket.add(product=product,qty=qty)
            basket.save()
            self.assertEqual(run+1,len(basket.basket["items"]),f"Test Basket has {run} items")
            self.assertEqual(product.price*qty,basket.basket["items"][str(product.pk)]["total_price"])
        self.assertEqual(runs,basket.basket["items"].__len__())
        # add anorther product
        rand=random.randint(1,10)
        basket.add(product=product,qty=rand)
        basket.save()
        self.assertEqual(qty+rand,basket.basket["items"][str(product.pk)]["qty"])
    def test_add_zero_qty(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        product=self.create_product()
        basket.add(product=product,qty=0)
        basket.save()
        self.assertEqual(0,len(basket.basket["items"]))
    def test_basket_len_items(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        runs=random.randint(1,10)
        total=0
        for run in range(runs):
            qty=random.randint(1,10)
            product=self.create_product()
            basket.add(product=product,qty=qty)
            basket.save()
            total+=qty
        self.assertEqual(total,basket.__len__())
    def test_basket_update(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        runs=random.randint(1,100)
        for run in range(runs):
            qty=random.randint(1,100)
            product=self.create_product()
            ##first add the items
            basket.add(product=product)
            #update
            basket.update(productid=product.pk,productqty=qty)
            basket.save()
            #after update quantity of the product should equal 
            self.assertEqual(qty,basket.basket["items"][str(product.pk)]["qty"])
    def test_delete_basket_items(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        runs=random.randint(1,100)
        for run in range(runs):
            qty=random.randint(1,100)
            product=self.create_product()
            basket.add(product=product,qty=qty)
            # reduce product quantity by
            basket.delete(product.pk)
            #should equal quantity less 1
            self.assertEqual(qty-1,basket.basket["items"][str(product.pk)]["qty"])
    def test_check_out(self):
        request=self.client.request()
        basket=self.create_Basket(request)
        product=self.create_product()
        basket.add(product=product)
        basket.checkout()
        self.assertTrue(basket.ordered)


class CartViewSetTestCase(TestCase):
    def setUp(self) -> None:
        self.user=get_user_model().objects.create(
                                    email="test@gmail.com",
                                    password="password",
                                    username="testuser")
        self.factory=APIRequestFactory()
        
    def create_product(self):
        return baker.make("Product")
    
    def add_request_session(self,request):
        ##add session
        middleware=SessionMiddleware()
        middleware.process_request(request=request)
        request.session.save()
            
    def test_add_item_to_cart(self):
        qty=random.randint(1,10)
        product=self.create_product()
        request=self.factory.post("/add_item_to_cart",data={"productid":product.pk,"productqty":qty})
        response=CartView.as_view(actions={"post":"add_item_to_cart"})(request)
        
        # user not logged in expect unauthorized
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,response.status_code)
        
        #log in the user
        request.user=self.user
        ##add session
        self.add_request_session(request=request)
        response=CartView.as_view(actions={"post":"add_item_to_cart"})(request)
        
        #now every thing should be ok
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertIsNotNone(response.data)
        
        #added only one product
        self.assertEqual(1,len(response.data["details"]["items"]))
        
        #add not existent product
        
        request=self.factory.post("/add_item_to_cart",data={"productid":1000,"productqty":qty})
        ##add session
        request.user=self.user
        self.add_request_session(request=request)     
        response=CartView.as_view(actions={"post":"add_item_to_cart"})(request)
        
        self.assertEqual(status.HTTP_404_NOT_FOUND,response.status_code)
        self.assertEqual("Given Product ID Not Found",response.data["message"])
    def test_update_cart_item(self):
        #create 5 products
        products=[self.create_product() for i in range(random.randint(1,5))]
        for product in products:
            qty=random.randint(1,15)
            request=self.factory.post("/add_item_to_cart",data={"productid":product.pk,"productqty":qty})
            request.user=self.user
            self.add_request_session(request=request)
            
        #choose a random product and update quantity
        product=random.choice(products)
        qty=qty=random.randint(1,15)
        
        #process the request        
        request=self.factory.put("/update_cart_item",data={"productid":product.pk,"productqty":qty})
        request.user=self.user
        self.add_request_session(request=request)
        
        response=CartView.as_view(actions={"put":"update_cart_item"})(request)
        
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        
        ##in our response check for our product and assert the quantity reflects
        [self.assertEqual(qty,item["qty"]) for item in response.data["details"]["items"] if item["qty"]==product.pk ]
        
        
        
        
            
            
        
        
        
        
        
        
        
        