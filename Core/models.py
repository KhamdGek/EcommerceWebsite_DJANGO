from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Define category tuple and label tuple 
CATEGORY_CHOICES= (
    ('S','Shirt'),
    ('SW','Sport Wear'),
    ('OW','OutWear')
)

LABEL_CHOICES= (
    ('D','danger'),
    ('P','primary'),
    ('s','secondary')
)

# Create your models here.

class Item(models.Model):
    title= models.CharField(max_length=100)
    price= models.FloatField()
    discount_price=models.FloatField(null=True)
    category= models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    label=models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug= models.SlugField()
    description=models.TextField()
    
    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug':self.slug
        })

    def remove_from_cart_url(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug':self.slug
        })


class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE, blank=True, null=True)
    item= models.ForeignKey(Item, on_delete=models.CASCADE)
    Ordered= models.BooleanField(default=False)
    quantity = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_Total_itemPrice(self):
        return self.quantity * self.item.price
        
    def get_TotalDiscounted_itemPrice(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_Total_itemPrice() - self.get_TotalDiscounted_itemPrice()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_TotalDiscounted_itemPrice()
        else:
            return self.get_Total_itemPrice()

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    items= models.ManyToManyField(OrderItem)
    start_date= models.DateTimeField(auto_now_add=True)
    ordered_date= models.DateTimeField()
    Ordered= models.BooleanField(default=False)
    billing_address=models.ForeignKey('Billingaddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_Total_order_price(self):
        total=0
        for itemorder in self.items.all():
            total += itemorder.get_final_price()
        return total

class Billingaddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    apartment_address=models.CharField(max_length=100)
    country=CountryField(multiple=False)
    Zip=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

