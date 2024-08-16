from django.db import models
from category.models import Category


class Product (models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug  = models.SlugField(max_length=100,unique=True)
    description = models.CharField(max_length=1000,unique=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_avilable = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    