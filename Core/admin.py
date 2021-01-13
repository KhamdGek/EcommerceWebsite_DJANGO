from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem, Item, Billingaddress

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Billingaddress)
