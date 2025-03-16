from store.models import Product, UserProfile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # get the current session key
        cart = self.session.get('session_key')
        # if user is new, then create a new session key
        if 'session_key' not in request.session:
            cart = self.session['session_key'] ={}

        # make cart global
        self.cart = cart

    def cart_total(self):
        product_id = self.cart.keys()

        products = Product.objects.filter(id__in=product_id)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total

    def retrieve(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            carted = str(self.cart)
            carted = carted.replace("\'", "\"")
            current_user.update(carted=str(carted))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
        #for logged in user
        if self.request.user.is_authenticated:
            current_user = UserProfile.objects.filter(user__id=self.request.user.id)
            carted = str(self.cart)
            carted = carted.replace("\'", "\"")
            current_user.update(carted=str(carted))


    def __len__(self):
        return len(self.cart)

    def summary(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def quantity(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id =  str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        now = self.cart
        return now






