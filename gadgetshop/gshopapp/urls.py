from django.urls import path
from gshopapp.views import base_view, product_view, category_view

urlpatterns = [
    path('', base_view, name='base'),
    path('product/<slug:product_slug>', product_view, name='product_detail'),
    path('category/<slug:category_slug>', category_view, name='category_detail'),
]