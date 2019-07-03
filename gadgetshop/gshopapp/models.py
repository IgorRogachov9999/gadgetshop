from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit

class Category(models.Model):
    
    name = models.CharField(max_length=100) 
    slug = models.SlugField(blank=True)


    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        try:
            translited = translit(instance.name, reversed=True)
        except:
            translited = instance.name
        instance.slug = slugify(translited)


pre_save.connect(pre_save_category_slug, sender=Category)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{}/{}".format(instance.slug, filename)


class ProductManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):

    category = models.ForeignKey(Category, models.CASCADE)
    brand = models.ForeignKey(Brand, models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = ProductManager()


    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})


class CartItem(models.Model):

    product = models.ForeignKey(Product, models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


    def __str__(self):
        return "Cart item for {}".format(self.product.title)
    

class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank=True)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


    def __str__(self):
        return str(self.id)