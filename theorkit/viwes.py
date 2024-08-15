# from django.http import render
from django.shortcuts import render

def home(request):
    return render(request,'home.html')