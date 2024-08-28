from django.shortcuts import render, redirect ,get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account,UserProfile
from orders.models import OrderProduct
from carts.models import Cart,CartItem
from orders.models import Order
from django.contrib import messages,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id

import requests


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
             
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,  email=email, phone_number=phone_number, password=password,username=username)
            user.save()


            #  User activations 
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request," Thannks for resustering   with us Veriyctatuin your email  ")
            return redirect('/accounts/login/?command=varification&email='+email)
        
    else:
        form = RegistrationForm()
    context = {
        'form': form 
    }
    return render(request,'accounts/register.html',context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None
    

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, " Congratulations ! Account is Active Login now ")
        return redirect('login')
    else:
        messages.error(request, " Invalid active link ")
        return redirect('register')


def  login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
       
        if user is not None:
            try:  
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()


                ex_var_list = []
                if  is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #Getiing the product variations by cart id 
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))


                    # Get The cart items from the user to access his porduct variations
                    
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # now we have    product_variation = [1,3,4,5,5]
                    # and also we have Ecestig  list = like = [2,3,5,6] 
                    # now migrate the value of  excesting variatin comon are shoulbe increse and others added to new cart
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index =  ex_var_list.index(pr)
                            item_id = id[index]
                            item =  CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user  = user
                                item.save()

                       
            except:
                pass 


            auth.login(request,user)
            messages.success(request,"You are now loged in")
            url = request.META.get('HTTP_REFERER')
            try:
                quary =  requests.utils.urlparse(url).query
                pramas = dict(x.split('=') for x in quary.split('&'))
                if 'next' in pramas:
                    nextPage =pramas['next']
                    return redirect(nextPage)

            except:
                return redirect('dashboard')
        else:
            messages.error(request,"Invalide Login ")
            return redirect('login')
    return render(request,'accounts/login.html')



@login_required(login_url = "login")
def  logout(request):
    auth.logout(request)
    messages.success(request,"you are loged out")
    return redirect('login')



@login_required(login_url = "login")
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    userprofile = get_object_or_404(UserProfile,user=request.user)   

    order_count = orders.count()
    context = {
        'order_count':order_count,
        'orders':orders,
        'userprofile':userprofile
        
    }
    return render(request, 'accounts/dashboard.html',context)




@login_required(login_url = "login")
def my_orders(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)

    context = {
        'orders':orders,
    }
    
    return render(request, 'accounts/my_orders.html',context)

@login_required(login_url = "login")
def edit_profile(request):  
    userprofile = get_object_or_404(UserProfile,user=request.user)   
    if request.method =='POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('edit_profile')
    else :
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'userprofile':userprofile

    }
    return render(request, 'accounts/edit_profile.html',context)

@login_required(login_url = "login")
def update_password(request):  
    if request.method == 'POST':
        current_password = request.POST['current_password']
        update_password = request.POST['update_password']
        confirm_password = request.POST['confirm_password']
    
        user = Account.objects.get(username__exact = request.user.username )
        if update_password ==confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(update_password)
                user.save()
                messages.success(request, "Password successfully updated ")
                return redirect('dashboard')
            else:
                messages.error(request,'Enter the valid cuttent password')
                return redirect('update_password')
        else:
            messages.error(request,"Password  Does not match")
            return redirect('update_password')
    return render(request, 'accounts/update_password.html')


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user= Account.objects.get(email__exact = email)

     
            #  Forget Passeord Email

            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/reset_password_validation.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()   
            return redirect('login')    
        else:
            messages.error(request, 'Account does not Exist !')     
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')


def reset_password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
        
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,"Reset Your password")
        return redirect('resetPassword')
    else:
        messages.error(request,"this link is expired")
        return redirect('login')
    
def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password =  request.POST['confirm_password']
        if password ==confirm_password:
            uid = request.session.get('uid')
            user =  Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Rese password Successful")
            return redirect('login')

        else:
            messages.error(request,"Password do not metch")
            return redirect('resetPassword')

    else:
        return render(request,'accounts/resetPassword.html')
    
@login_required(login_url = "login")
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }

    return render(request,'accounts/order_detail.html')