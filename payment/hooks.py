from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings
import time

from payment.models import Order


@receiver(valid_ipn_received)
def paypay_payment(sender, **kwargs):
    time.sleep(4)
    ipn_object = sender

    my_invoice = str(ipn_object.invoice)
    my_order = Order.objects.get(invoice=my_invoice)
    my_order.paid = True
    my_order.save()

