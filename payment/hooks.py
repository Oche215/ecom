from django.shortcuts import redirect
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time

from payment.models import Order
from payment.views import payment_success


@receiver(valid_ipn_received)
def paypal_payment(sender, **kwargs):
    time.sleep(4)
    ipn_object = sender

    # Extract data from ipn_object
    transaction_id = ipn_object.txn_id
    payment_status = ipn_object.payment_status
    amount = ipn_object.mc_gross
    payer_email = ipn_object.payer_email

    my_invoice = str(ipn_object.invoice)
    my_order = Order.objects.get(invoice=my_invoice)

    my_order.paid = True
    my_order.save()

    return redirect('payment_success', transaction_id, payment_status, amount, payer_email, my_invoice)



