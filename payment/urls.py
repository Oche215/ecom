from django.urls import path, include
from .views import payment, checkout, billing, process_order, shipped_dash, not_shipped_dash, orders, payment_success, payment_failed

urlpatterns = [

    path('', payment, name="payment"),

    path('payment_success', payment_success, name="payment_success"),
    path('payment_failed', payment_failed, name="payment_failed"),

    path('checkout/', checkout, name="checkout"),
    path('billing/', billing, name="billing"),
    path('process_order/', process_order, name="process_order"),
    path('shipped_dash/', shipped_dash, name="shipped_dash"),
    path('not_shipped_dash/', not_shipped_dash, name="not_shipped_dash"),
    path('orders/<int:pk>', orders, name="orders"),
    path('paypal', include('paypal.standard.ipn.urls')),

    ]