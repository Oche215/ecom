from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    products = cart.summary()
    quantities = cart.quantity
    totals = cart.cart_total()
    messages.success(request, "Welcome to your Cart Summary, review your orders adn proceed to checkout!")
    return render(request, 'cart/cart_summary.html', {'products': products, 'quantities': quantities, 'totals': totals})

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Lookup product in db
        product = get_object_or_404(Product, id=product_id)
        #save to session
        cart.add(product=product, quantity=product_qty)
        #get Cart quantity
        cart_qty = cart.__len__()

        # return a response
        #response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_qty})
        messages.success(request, "Product successfully added to Cart!")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuff
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id })
        messages.success(request, "Product successfully deleted from Cart!")
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get Stuffpr
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Lookup product in db
        product = get_object_or_404(Product, id=product_id)
        #save to session
        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, "Product successfully updated to Cart!")
        return response

