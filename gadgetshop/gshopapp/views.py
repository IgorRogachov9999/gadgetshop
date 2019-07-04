from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from gshopapp.forms import OrderForm
from gshopapp.models import Category, Product, CartItem, Cart, Order


def get_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
    return cart


def base_view(request):
    cart = get_cart(request)
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'base.html', context)
    

def product_view(request, product_slug):
    cart = get_cart(request)
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'cart': cart
    }
    return render(request, 'product.html', context)


def category_view(request, category_slug):
    cart = get_cart(request)
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
    cart = get_cart(request)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'cart.html', context)


def add_to_cart_view(request):
    cart = get_cart(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    data = {
        'cart_total': cart.items.count(),
        'cart_total_price': new_cart_total
    }
    return JsonResponse(data)


def remove_from_cart_view(request):
    cart = get_cart(request)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product)
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    data = {
        'cart_total': cart.items.count(),
        'cart_total_price': new_cart_total
    }
    return JsonResponse(data)


def change_item_qty_view(request):
    cart = get_cart(request)
    qty = int(request.GET.get('qty'))
    item_id = int(request.GET.get('item_id'))
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.qty = qty
    cart_item.item_total = qty * float(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    data = {
        'cart_total': cart.items.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': new_cart_total
    }
    return JsonResponse(data)


def checkout_view(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'checkout.html', context)


def thank_you_view(request):
    cart = get_cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'thank_you.html', context)


def order_create_view(request):
    cart = get_cart(request)
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comments = form.cleaned_data['comments']
        order = Order()
        order.user = request.user
        order.save()
        order.items.add(cart)
        order.last_name = last_name
        order.phone = phone
        order.buying_type = buying_type
        order.address = address
        order.comments = comments
        order.total = cart.cart_total
        order.save()
        del request.session['cart_id']
        del request.session['total']
        return HttpResponseRedirect(reverse('thank_you'))
    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'order.html', context)

