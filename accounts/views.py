from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
            user.is_active = True
            user.save()
            messages.success(request,"Registration Succesfull")
            return redirect('login')
        
    else:
        form = RegistrationForm()
    context = {
        'form': form 
    }
    return render(request,'accounts/register.html',context)




def  login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
       
        
        if user is not None:
            auth.login(request,user)
            # messages.success('Your are Logedin ')
            return redirect('home')
        else:
            messages.error(request,"Invalide Login ")
            return redirect('login')
    return render(request,'accounts/login.html')



@login_required(login_url = "login")
def  logout(request):
    auth.logout(request)
    messages.success(request,"you are loged out")
    return redirect('login')