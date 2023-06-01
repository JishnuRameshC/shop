from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem,Order, OrderItem
from datetime import datetime
from django.db.models import F, Sum
from django .urls import reverse



from django.contrib import messages
# Create your views here.
def calculate_total(price, quantity):
    return price * quantity


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

    # Retrieve the items in the cart and order them by their ID or any other desired criteria
    items = cart.cartitem_set.all().order_by('id')

    # Calculate the total price for each item
    for item in items:
        item.total_price = item.product.price * item.quantity

    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'app1/cart.html', context)


def order(request, product_id):
    # Retrieve the product
    product = get_object_or_404(Product, pk=product_id)

    # Create a new cart or retrieve the existing cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create a new cart item and associate it with the product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Increase the quantity of the cart item by 1
    cart_item.quantity += 1
    cart_item.save()

    # Calculate the total price of the cart
    cart.total_price += product.price
    cart.save()

    # Redirect to the cart view
    return redirect('view-cart')


def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    # Rest of the view logic

    return render(request, 'app1/place_order.html', {'total_price': total_price})


def submit_order(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Create the order object
        order = Order(name=name, email=email, address=address, city=city, state=state, zipcode=zipcode)
        order.save()

        # Clear the cart or perform any additional actions

        # Redirect to a success page
        return redirect('order_success')

    # If the request is not POST, render the submit-order template
    return render(request, 'submit_order.html')


def order_success(request):
    order = Order.objects.last() 
    return render(request, 'app1/order_success.html', {'order': order})


def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')
    return render(request, 'app1/order_history.html', {'orders': orders})

def thank_you(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'app1/thank_you.html', {'order': order})



