from django.db import models
from django.conf import settings
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

    
    def add_to_cart(self, product):
        new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in self.items.all():
            self.items.add(new_item[0])
            self.save()
    

    def remove_from_cart(self, product):
        for cart_item in self.items.all():
            if cart_item.product == product:
                self.items.remove(cart_item)
                self.save()


ORDER_STATUS_CHOICES = (
    ('In processing', 'In processing'),
    ('Performed', 'Performed'),
    ('Paid', 'Paid')
)

DELIVERY_CHOICES = (
    ('Pickup', 'Pickup'), 
    ('Delivery', 'Delivery')
)


class Order(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    items = models.ManyToManyField(Cart)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    addres = models.CharField(max_length=255)
    buing_type = models.CharField(max_length=32, choices=DELIVERY_CHOICES,
                                  default=DELIVERY_CHOICES[0][1])
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
    status = models.CharField(max_length=64, choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_CHOICES[0][1])


    def __str__(self):
        return "Order #{}".format(str(self.id))