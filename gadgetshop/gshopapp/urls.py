from django.urls import path
from gshopapp.views import (base_view, 
                           product_view, 
                           category_view, 
                           cart_view, 
                           add_to_cart_view, 
                           remove_from_cart_view, 
                           change_item_qty_view, 
                           checkout_view,
                           order_create_view,
                           thank_you_view)
                        

urlpatterns = [
    path('', base_view, name='base'),
    path('product/<slug:product_slug>', product_view, name='product_detail'),
    path('category/<slug:category_slug>', category_view, name='category_detail'),
    path('add_to_cart/', add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', change_item_qty_view, name='change_item_qty'),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', order_create_view, name='create_order'),
    path('thank_you/', thank_you_view, name='thank_you'),
    path('cart/', cart_view, name='cart'),
]