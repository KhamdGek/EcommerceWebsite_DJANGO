from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import (
    HomeView,
    OrderSummaryView,
    ItemDetailView,
    Checkout_Page,
    add_to_cart,
    remove_from_cart,
    remove_Item_from_cart,
    add_item_to_cart,
    PayementView
)

urlpatterns = [
    path('', HomeView.as_view(), name='Home'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/',  Checkout_Page.as_view(), name=' Checkout_Page'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>',remove_from_cart, name='remove_from_cart'),
    path('remove_Item_from_cart/<slug>',remove_Item_from_cart, name='remove_Item_from_cart'),
    path('add_item_to_cart/<slug>',add_item_to_cart, name='add_item_to_cart'),
    path('payment/<payement-option>/', PayementView.as_view(), name='Payemnt')
]