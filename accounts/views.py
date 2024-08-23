from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
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

from carts.models import Cart,CartItem
from carts.views import _cart_id



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
                if  is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user= user
                        item.save()

            except:
                pass 


            auth.login(request,user)
            messages.success(request,"you are loged in")
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
    return render(request, 'accounts/dashboard.html')

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