from django.shortcuts import render
from .models import Product
# Create your views here.


def home(request):
    return render(request,"app1/product.html")

def product_list(request):
    products = Product.objects.all()
    return render(request,'app1/product_list.html',{'products':products})