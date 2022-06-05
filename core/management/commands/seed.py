import json
import requests

from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

from taggit.managers import TaggableManager

from product.models import Product,ProductRating
from category.models import Category

path="https://fakestoreapi.com/products"

def get_image_from_url(url):
       img_tmp = NamedTemporaryFile()
       with requests.get(url,stream=True) as uo:
           assert uo.status_code == requests.codes.ok
           for block in uo.iter_content(1024 * 8):
               if not block:
                    break
               img_tmp.write(block)
       img = File(img_tmp)
       return img

def seed_products():        
    print(f"\nfetching dummy items.................from {path}",end="\n")
    with requests.get(path) as resp:
        count=0
        for item in resp.json():
            print(f"fetching item....{count+1} of 20",end="\r")
            product=Product()
            obj,created=Category.objects.get_or_create(title=item["category"])
            product.title=item["title"]
            product.price=item["price"]
            product.description=item["description"]
            product.category=obj
            ratings=ProductRating()
            ratings.rate=item["rating"]["rate"]
            ratings.count=item["rating"]["count"]
            ratings.save()
            product.ratings=ratings
            file_name = item["image"].split("/")[-1]
            product.image.save(file_name,get_image_from_url(item["image"]))
            product.save()
            [product.tags.add(i) for i in item["title"].split(" ")]
            product.save()
            count+=1
        resp.close()
        print("Finished Fetching items....")
        print()
        print(f"Fetched {count} items")


def clear_data():
    Product.objects.all().delete()
    Category.objects.all().delete()
    ProductRating.objects.all().delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        #flush the db
        try:
            clear_data()
        except exception as e:
            print("could not flush db...",e)
        #fetch new items
        try :
            seed_products()
            print("completed")    
        except KeyError as e:
            print("could not fetch items...",e)
