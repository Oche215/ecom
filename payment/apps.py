from django.apps import AppConfig
from django.core.signals import request_finished


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    #setup paypay IPN signal
    def ready(self):
        # import payment.hooks

        from .hooks import paypal_payment
        request_finished.connect(paypal_payment)

