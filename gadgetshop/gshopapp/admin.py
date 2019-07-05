from django.contrib import admin
from gshopapp.models import Category, Brand, Product, CartItem, Cart, Order, ORDER_STATUS_CHOICES


def make_payed(modeladmin, request, queryset):
    queryset.update(status=ORDER_STATUS_CHOICES[2])
make_payed.short_description = 'Mark as payed'


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
