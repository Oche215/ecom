from django.urls import path
from .views import payment, checkout, billing, process_order, shipped_dash, not_shipped_dash, orders

urlpatterns = [

    path('', payment, name="payment"),
    path('checkout/', checkout, name="checkout"),
    path('billing/', billing, name="billing"),
    path('process_order/', process_order, name="process_order"),
    path('shipped_dash/', shipped_dash, name="shipped_dash"),
    path('not_shipped_dash/', not_shipped_dash, name="not_shipped_dash"),
    path('orders/<int:pk>', orders, name="orders"),

    ]