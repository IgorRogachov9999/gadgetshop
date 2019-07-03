from django.db import models

class Category(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField()


    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, models.CASCADE)
    brand = models.ForeignKey(Brand, models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)


    def __str__(self):
        return self.title