from .cart import Cart

# create contex processor
def cart(request):
    return {'cart': Cart(request)}
