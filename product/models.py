from io import BytesIO
from itertools import product
from PIL import Image
import random,string
import os


# Create your models here.
from django.db import models
from django.core.files import File
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver

from rest_framework.reverse import reverse

#to easily manage tags
#phweks lifesaver !!
from taggit.managers import TaggableManager
from category.models import Category

from core.models import EnablePartialUpdateMixin

class ProductRating(models.Model):
    rate=models.FloatField()
    count=models.IntegerField()

PRODUCT_LABEL=(
    ("NEW","NEW"),
    ("REFURBISHED","REFURBISHED")
)

# BASE_URL=reverse("core-api")  

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
  
#product
class Product(models.Model,EnablePartialUpdateMixin):
    """
    Stores a single Product entity
    """
    title=models.CharField(max_length=100,help_text="the title of the product")
    description=models.TextField(blank=True,help_text="description of the product")
    category=models.ForeignKey(to=Category,on_delete=models.CASCADE,related_name="product",help_text="the categeory this product belongs to")
    price=models.DecimalField(decimal_places=2,max_digits=6,help_text="The price of the product")
    label=models.CharField(max_length=20,choices=PRODUCT_LABEL,blank=False)
    image=models.ImageField(upload_to="uploads/",blank=True) ##add height and width
    thumbnail=models.ImageField(upload_to="uploads/",blank=True,editable=False)
    created=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(max_length=30,editable=False,blank=True)
    objects=models.Manager()
    tags=TaggableManager()
    products = ProductManager()
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    ratings=models.OneToOneField(to=ProductRating,on_delete=models.DO_NOTHING,blank=True,null=True)

    class Meta:
        ordering=["created"]
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("product-list")+f"?slug={self.slug}"
    def get_image(self):
        if self.image:
            return reverse("core-api").rstrip("/") + self.image.url
        return ""
    def get_thumbnail(self):
        if self.thumbnail:
            return reverse("core-api").rstrip("/")+self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save()

                return reverse("core-api").rstrip("/")+self.thumbnail.url
            else:
                return ""

    def make_thumbnail(self,image,size=(300,200)):
        img=Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io=BytesIO()
        img.save(thumb_io,"JPEG",quality=85)

        thumbnail=File(thumb_io,name=f"{image.name}.jpg")

        return thumbnail

    def save(self,*args, **kwargs):
        self.slug=self.generate_slug(self.title)
        super().save(*args,**kwargs)

    def generate_slug(self,add_random_suffix=True):
        """
        Generate and returns slugs for this obj.

        Note: setting `save_to_obj` to True when called 
              from `.save` method 
              can lead to recursion error
        add random suffix to make sure that slug field has unique value
         
         """

        generated_slug=slugify(self.title)

        # generate a random slug
        random_suffix=""
        if add_random_suffix:
            random_suffix="".join([random.choice(string.ascii_letters+string.digits) for i in range(5)])
            generated_slug+= f"-{random_suffix }"    
        return generated_slug

# delete images if a record is delete
@receiver(models.signals.post_delete, sender=product)
def delete_product_image(sender,instance=None,*args, **kwargs):
    if instance is not None:
        print(instance.image.path)
        if instance.image:
            _delete_file(instance.image.path)
        if instance.thumbnail:
            _delete_file(instance.thumbnail.path)    
def _delete_file(path):
    if os.path.isfile(path):
        os.remove(path=path)

