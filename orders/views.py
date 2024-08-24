from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from  .forms import OrderForm
from .models import Order
from carts import views
import datetime

def place_order(request, total=0,   fee = 0,  grand_total = 0, quantity=0):

    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store',total=0, quantity=0)
    
   


    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    fee = 120
    grand_total = total + fee


    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data. order_total = grand_total
            data.fee = fee
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr= int(datetime.date.today().strftime('%Y'))
            dt= int(datetime.date.today().strftime('%d'))
            mt= int(datetime.date.today().strftime('%m'))
            d =  datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date+str(data.id)
            data.order_number= order_number
            data.save()
            return redirect('checkout')
    else:
               
        return redirect ('dashboard')
