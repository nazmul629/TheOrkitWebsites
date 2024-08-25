from django.shortcuts import render,get_object_or_404, redirect
from .models import Product,ReviewRating,ProductGallery
from carts.models import CartItem
from category.models import Category
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages,auth



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
    
    reviews = ReviewRating.objects.filter(product_id = single_product.id, status = True)
    product_gallery = ProductGallery.objects.filter(product_id = single_product.id)
    context={
        "single_product":single_product,
        'in_cart':in_cart,
        'reviews':reviews,
        "product_gallery":product_gallery,

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


def submit_review(request, product_id):
     url = request.META.get('HTTP_REFERER')
     if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
            
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.product = product_id
                data.user = request.user.id
                data.subject = form.changed_data['subject']
                data.review = form.changed_data['review']
                data.rating = form.changed_data['rating']
                data.ip = request.META.get("REMOTE_ADDR")
                data.save()
                messages.success(request,"Thank you , Your review is updated !")
                return redirect(url)

   
