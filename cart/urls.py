from django.urls import path
from .views import cart_summary, cart_add, cart_delete, cart_update

urlpatterns = [
    path('update/', cart_update, name="cart_update"),
    path('delete/', cart_delete, name="cart_delete"),
    path('add/', cart_add, name="cart_add"),
    path('', cart_summary, name="cart_summary"),

]