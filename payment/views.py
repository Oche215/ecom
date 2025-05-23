from locale import currency

from django.core.signals import request_finished
from django.shortcuts import render, redirect
from django.template.context_processors import request

from cart.cart import Cart
from django_project.settings import PAYPAL_RECEIVER_EMAIL
from store.models import UserProfile
from .admin import OrderItemInline
from .models import ShippingAddress, Order, OderItem
from .forms import ShippingAddressForm, PaymentForm
from store.forms import UserProfileForm
from django.contrib import messages
import datetime

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.models import PayPalIPN

from django.conf import settings
import uuid #unique user_id for duplicate orders


# Create your views here.
def payment(request):

    return render(request, 'payment/payment.html', {})


def checkout(request):
    cart = Cart(request)
    products = cart.summary()
    quantities = cart.quantity
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user )

        return render(request, 'payment/checkout.html',{'products': products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        #checkout as guest

        shipping_form = ShippingAddressForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'products': products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})



def billing(request):
    if request.POST:

        cart = Cart(request)
        products = cart.summary
        quantities = cart.quantity
        totals = cart.cart_total()

        my_shipping =request.POST
        request.session['my_shipping'] = my_shipping

        host = request.get_host()
        #paypal stuff
        my_invoice = str(uuid.uuid4())

        paypal_dict = {
            'business': PAYPAL_RECEIVER_EMAIL,
            'amount': totals,
            'item_name': 'Confectionery Order',
            'no_shipping': '2',
            'invoice': my_invoice,
            'currency_code': 'USD',
            'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'https://{}{}'.format(host, reverse('payment_success')),
            'cancel_return': 'https://{}{}'.format(host, reverse('payment_failed')),

        }

        #create PayPal button
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)


        if request.user.is_authenticated:
            shipping_form = request.POST
            billing_form = PaymentForm()

            # create pre Order
            payment_form = PaymentForm(request.POST or None)
            # GEt shipping session stuff
            my_shipping = request.session.get('my_shipping')
            shipping_address = f"{my_shipping['Shipping_address1']}\n {my_shipping['Shipping_address2']}\n {my_shipping['Shipping_city']}\n {my_shipping['Shipping_state']}\n {my_shipping['Shipping_zipcode']}\n {my_shipping['Shipping_country']}\n"

            # gather order info
            full_name = my_shipping['Shipping_full_name']
            email = my_shipping['Shipping_email']
            amount = totals

            # create order
            if request.user.is_authenticated:
                user = request.user
            else:
                user = None
                create_order = Order(user=user, full_name=full_name, email=email, Shipping_address=shipping_address,
                                 amount=amount, invoice=my_invoice)
                create_order.save()

                # add order item
                order_id = create_order.pk

                for product in products():
                    product_id = product.id
                    if product.is_sale:
                        price = product.sale_price
                    else:
                        price = product.price

                    for key, value in quantities().items():
                        if int(key) == product_id:
                            quantity = value
                            create_order_item = OderItem(order_id=order_id, product_id=product_id, user=user,
                                                         quantity=quantity,
                                                         price=price)
                            create_order_item.save()

            return render(request, 'payment/billing.html', {'paypal_form': paypal_form, 'products': products, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form, 'billing_form': billing_form, 'my_shipping': my_shipping})
        else:
            shipping_form = request.POST
            billing_form = PaymentForm()
            return render(request, 'payment/billing.html',
                          {'products': products, 'quantities': quantities, 'totals': totals,
                           'shipping_form': shipping_form, 'billing_form': billing_form, 'paypal_form': paypal_form})

    else:
        messages.success(request, 'You do not have a valid cart.')
        return redirect('home')


def process_order(request):
    cart = Cart(request)
    products = cart.summary
    quantities = cart.quantity
    totals = cart.cart_total()

    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        #GEt shipping session stuff
        my_shipping = request.session.get('my_shipping')
        shipping_address = f"{ my_shipping['Shipping_address1']}\n { my_shipping['Shipping_address2']}\n { my_shipping['Shipping_city']}\n { my_shipping['Shipping_state']}\n { my_shipping['Shipping_zipcode']}\n { my_shipping['Shipping_country']}\n"

        #gather order info
        full_name = my_shipping['Shipping_full_name']
        email = my_shipping['Shipping_email']
        amount = totals

        #create order
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        create_order = Order(user=user, full_name=full_name, email=email, Shipping_address=shipping_address, amount=amount)
        create_order.save()

        #add order item
        order_id = create_order.pk
        for product in products():
            product_id = product.id
            if product.is_sale:
                price = product.sale_price
            else:
                price = product.price

            for key, value in quantities().items():
                if int(key) == product_id:
                    quantity = value
                    create_order_item = OderItem(order_id=order_id, product_id=product_id, user=user, quantity=quantity, price=price)
                    create_order_item.save()

        #rest Cart after checkout
        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]
                cart = request.session['session_key'] = {}
                current_user = UserProfile.objects.filter(user__id=request.user.id)
                carted = str(cart)
                current_user.update(carted=carted)

        messages.success(request, 'order places')
        return redirect('home')
    else:
        messages.success(request, 'access denied')
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            now = datetime.datetime.now()

            order = Order.objects.filter(id=num)
            order.update(shipped=False, date_shipped=None)


            messages.success(request, 'Shipping Status Updated!')

        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'access denied')
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']

            now = datetime.datetime.now()

            order = Order.objects.filter(id=num)
            order.update(shipped=True, date_shipped=now)


            messages.success(request, 'Shipping Status Updated!')


        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'access denied')
        return redirect('home')


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            now = datetime.datetime.now()
            if status == 'true':
                order = Order.objects.filter(id=pk)
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False, date_shipped=None)

            messages.success(request, 'Shipping Status Updated!')
            return redirect('orders', pk )


        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.success(request, 'access denied')
        return redirect('home')


def payment_success(request):
    my_paypal = request.GET
    request.session['my_paypal'] = my_paypal
    paypal_info = request.session.get('my_paypal')

    # invoice = paypal_info.invoice



    for key, value in paypal_info.items():

        if key == "invoice":
            x = str(value)

            # ipn = PayPalIPN.objects.filter(invoice=x)
            # order = Order.objects.filter(invoice=x)
            #
            # # order_item = order.items.all()
            # items = order.orderitem_set.all()

            # reset Cart after checkout
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
                    cart = request.session['session_key'] = {}
                    if request.user.is_authenticated:
                        current_user = UserProfile.objects.filter(user__id=request.user.id)
                        carted = str(cart)
                        current_user.update(carted=carted)


            return render(request, 'payment/payment_success.html', {'paypal_info': paypal_info, 'x': x, 'value': value})

def payment_failed(request):
    return render(request, 'payment/payment_failed.html', {})