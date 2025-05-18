from django.contrib import admin
from .models import ShippingAddress, Order, OderItem
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OderItem)

class OrderItemInline(admin.StackedInline):
    model = OderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered", "date_shipped"]
    fields = ['user', 'full_name', 'email', 'shipping_address', 'amount', 'date_ordered', 'shipped', 'date_shipped', 'invoice', 'paid']
    inlines = [OrderItemInline]

#re-register the Order Model
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)