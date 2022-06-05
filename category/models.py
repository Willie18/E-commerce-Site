from django.db import models

# Create your models here.

#category
class Category(models.Model):
    title=models.CharField(max_length=20)
    description=models.TextField()
    slug=models.SlugField(blank=True,editable=False,max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Categories"
        ordering=["title"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/{self.slug}"
