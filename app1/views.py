from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.
app_name = 'app1'

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app1/product.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request,'app1/product_list.html',{'products':products})