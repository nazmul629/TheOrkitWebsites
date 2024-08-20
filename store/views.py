from django.shortcuts import render,get_object_or_404, redirect
from .models import Product
from carts.models import CartItem
from category.models import Category
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q



def store(request,category_slug=None):
    categories = None
    products=None


    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug )
        products = Product.objects.filter(category = categories, is_avilable = True)
      

    else:
        products = Product.objects.all().filter(is_avilable=True).order_by('id')
     


    product_count = products.count()

      # product paginator 
    paginator = Paginator(products,4)
    page = request.GET.get('page')
    paged_produts = paginator.get_page(page)

    context = {
        'products' : paged_produts, 
        'product_count':product_count,
        
    }

    return render(request,'store/store.html',context)



def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart =  CartItem.objects.filter(cart__cart_id= _cart_id(request),product= single_product).exists()

    except Exception as e :
        raise e 
    context={
        "single_product":single_product,
        'in_cart':in_cart
    }
    return render(request,'store/product-detail.html',context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        else: 
            return redirect('store')     
    
    context= {
        'products':products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)
