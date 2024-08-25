from django.contrib import admin
from.models import *
from django.contrib.auth.admin import UserAdmin




class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','first_name','phone','email','order_total','fee','status')
    filter_horizontal =()
    list_filter = ('order_number','email','phone','first_name')
    list_display_links =('order_number','first_name','phone','email')
  
admin.site.register(Order,OrderAdmin)# Register your models here.

admin.site.register(Payment),

admin.site.register(OrderProduct)

