from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem

from django.contrib import messages
# Create your views here.
app_name = 'app1'

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'app1/product.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request,'app1/product_list.html',{'products':products})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product already exists in the cart
    try:
        cart_item = cart.cartitem_set.get(product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the product doesn't exist, create a new CartItem
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    
    return redirect('view-cart')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()

    # Update the total price of the cart
    cart = item.cart
    cart.total_price += item.product.price
    cart.save()

    return redirect('view-cart')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        
        # Update the total price of the cart
        cart = item.cart
        cart.total_price -= item.product.price
        cart.save()
    else:
        item.delete()

    return redirect('view-cart')



def view_cart(request):
    # Retrieve the cart for the current user
    cart = get_object_or_404(Cart, user=request.user)

    # Retrieve the items in the cart
    items = cart.cartitem_set.all()

    # Calculate the total price for each item
    for item in items:
        item.total_price = item.quantity * item.product.price

    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'app1/cart.html', context)


