from django.shortcuts import render
from django.http import HttpResponseRedirect
from gshopapp.models import Category, Product, CartItem, Cart


def base_view(request):
    cart = Cart.objects.first()
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'base.html', context)
    

def product_view(request, product_slug):
    cart = Cart.objects.first()
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    cart = Cart.objects.first()
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category': category,
        'products_of_category': products_of_category,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'category.html', context)


def cart_view(request):
    cart = Cart.objects.first()
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)
    cart = Cart.objects.first()
    if new_item not in cart.items.all():
        cart.items.add(*new_item)
        cart.save()
    else:
        new_item = cart.items.get(product=product)
        print(new_item)
    return HttpResponseRedirect('/cart/')