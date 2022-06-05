import random
from django.test import TestCase


from rest_framework.test import APIRequestFactory

from rest_framework import status

from django.contrib.auth import get_user_model

from django.urls import reverse

from model_bakery import baker

from product.models import PRODUCT_LABEL, Product
from product.serializers import ProductSerializer
from product.views import ProductViewSet
from tokens import serializers

# Create your tests here.

class ProductTests(TestCase):
    def setUp(self):
        self.product=baker.make("product.Product")
    def test_create_product(self):
        self.assertIsNotNone(self.product)
        created_product=Product.objects.get(pk=self.product.pk)
        self.assertEqual(self.product,created_product)
        self.assertEqual(self.product.title,str(created_product))
        self.assertEqual(self.product.get_image(),"")
        self.assertEqual(self.product.get_absolute_url(),reverse("product-list")+"?slug="+self.product.slug)
        self.assertEqual(self.product.get_thumbnail(),"")

class ProductViewTest(TestCase):
    def setUp(self) -> None:
        self.factory=APIRequestFactory()
        self.view=ProductViewSet.as_view(actions={
            "get":"list",
            "post":"create",
            "delete":"destroy",
            "put":"update",
            "patch":"partial_update"
        })
        self.user=get_user_model().objects.create_user(
            "test@user.com","testuser","password"
        )
    def create_super_user(self):
        return get_user_model().objects.create_superuser("test@superuser.com","testsuperuser","password")
    def test_list_products(self):
        request=self.factory.get("/products")
        request.user=self.user
        response=self.view(request)

        self.assertEqual(status.HTTP_200_OK,response.status_code)


    def test_create_product(self):
        self.client.login(email="test@user.com",password="password")

        product=baker.make("Product",ratings=baker.make("ProductRating"))
        serializer=ProductSerializer(product)
        request=self.factory.post("/products",data=serializer.data,format="json")
        request.user=self.user
        response=self.view(request)

        self.assertFalse(request.user.has_perm("product_list"))
        self.assertEqual(status.HTTP_403_FORBIDDEN,response.status_code)

        ##CREATE SUPER USER

        superuser=self.create_super_user()

        #super user should create a product

        self.client.login(email="test@superuser.com",password="password")

        request=self.factory.post("/products",data=serializer.data,format="json")
        request.user=superuser
        self.assertTrue(superuser.has_perm("product_create"))
        response=self.view(request)

        self.assertEqual(status.HTTP_201_CREATED,response.status_code)
    
    def test_partial_update_product(self):
        superuser=self.create_super_user()
        


