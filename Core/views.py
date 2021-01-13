from django.shortcuts import render,get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist #used for checking if object is null or not
from django.contrib.auth.decorators import login_required #Cannot be used with class based views
from django.contrib.auth.mixins import LoginRequiredMixin #Used for Class based views 
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Billingaddress
from .forms import CheckoutForm
from django.utils import timezone
from django.contrib import messages 
# Create your views here.

class HomeView(ListView):
    model=Item 
    paginate_by= 12 
    template_name="home-page.html" 

class OrderSummaryView(LoginRequiredMixin, View):
   def get(self, *args, **kwargs):
       try:
           order=Order.objects.get(user=self.request.user, Ordered=False)
           context={
               'object': order
           }
           return render(self.request, 'order_summary.html', context)
       except ObjectDoesNotExist:
            message.error(self.request, "You do not have any active order at the moment!")
            return redirect('/')       

class ItemDetailView(DetailView):
    model=Item
    template_name ="product.html" 


class Checkout_Page(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        forms= CheckoutForm()
        context={
            'form': forms
        }
        return render(self.request,"checkout-page.html", context)

    def post(self, *args, **kwargs):
        forms= CheckoutForm(self.request.POST or None) 
        try:
            order= Order.objects.get(user=self.request.user, Ordered=False)
            if forms.is_valid():
                print(forms.cleaned_data)
                street_address=forms.cleaned_data('street_address')
                apartment_address=forms.cleaned_data('apartment_address')
                country=forms.cleaned_data('country')
                Zip=forms.cleaned_data('Zip')
                same_billing_address=forms.cleaned_data('same_billing_address')
                save_info=forms.cleaned_data('save_info')
                payment_options=forms.cleaned_data('payment_options')
                bilinaddress=Billingaddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    Zip=Zip
                )
                bilinaddress.save()
                Order.billing_address=bilinaddress
                Order.save()

                message.info(self.request, "The form is valid")
                return redirect('core:checkout')
            message.warning(self.request, "The form is not valid")
            return redirect('/')
        except ObjectDoesNotExist:
            message.error(self.request, "You do not have any active order at the moment!")
            return redirect('core:/')

class PayementView(View):
    def get(self,*args,**kwargs):
        return render(self.request, "payment.html")


@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item, slug=slug)
    Order_Item, created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        Ordered=False
        )
    order_qs= Order.objects.filter(user=request.user, Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # check if order already exits add the quantity up
        if order.items.filter(item__slug=item.slug).exists():
            Order_Item.quantity +=1
            Order_Item.save()
            messages.info(request, "Your order has been updated! Thank you for shopping")
        else:
            order.items.add(Order_Item)
    else:
        ordered_date = timezone.now()
        order= Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(Order_Item)
        messages.info(request, "Your order has been added to the cart! Thank you for shopping")
    return redirect("core:product", slug=slug)

@login_required
def remove_from_cart(request, slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs= Order.objects.filter(user=request.user, Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # check if order already exits add the quantity up
        if order.items.filter(item__slug=item.slug).exists():
            Order_Item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                Ordered=False
            )[0]
            order.items.remove(Order_Item)
            messages.info(request, "Your order has been removed to the cart!")
        else:
            messages.info(request, "You have no order at the moment!")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You have no active order at the moment!")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def remove_Item_from_cart(request, slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs= Order.objects.filter(user=request.user, Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # check if order already exits add the quantity up
        if order.items.filter(item__slug=item.slug).exists():
            Order_Item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                Ordered=False
            )[0]
            if Order_Item.quantity >1:
                Order_Item.quantity -=1
                Order_Item.save()
                messages.info(request, "Your order has been updated!")
                return redirect("core:order-summary")
            else:
                order.items.remove(Order_Item)
                messages.info(request, "You have no order at the moment!")
                return redirect("core:Home")
       
    else:
        messages.info(request, "You have no active order at the moment!")
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


@login_required
def add_item_to_cart(request,slug):
    item=get_object_or_404(Item, slug=slug)
    Order_Item, created=OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        Ordered=False
        )
    order_qs= Order.objects.filter(user=request.user, Ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        # check if order already exits add the quantity up
        if order.items.filter(item__slug=item.slug).exists():
            Order_Item.quantity +=1
            Order_Item.save()
            messages.info(request, "Your order has been updated!")
            return redirect("core:order-summary")
        else:
            messages.info(request, "You have no order at the moment!")
            return redirect("core:product")
    else:
        ordered_date = timezone.now()
        order= Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(Order_Item)
        messages.info(request, "Your order has been added to the cart! Thank you for shopping")
    return redirect("core:product", slug=slug)