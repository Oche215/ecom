from django.db import models
from django.contrib.auth.models import User
from django.db.models import Model

from store.models import Product, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Shipping_full_name = models.CharField(max_length=200)
    Shipping_email = models.CharField(max_length=200)
    Shipping_address1 = models.CharField(max_length=200)
    Shipping_address2 = models.CharField(max_length=200, null=True, blank=True)
    Shipping_city = models.CharField(max_length=200)
    Shipping_state = models.CharField(max_length=200, null=True, blank=True)
    Shipping_zipcode = models.CharField(max_length=200, null=True, blank=True)
    Shipping_country = models.CharField(max_length=200)

    #unpluralize Address
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


# create Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, )
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Shipping_address = models.TextField(max_length=1500)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)
    #PayPal Invoice and Paid T/F
    invoice = models.CharField(max_length=250, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order - {str(self.id)}'

    #auto add shipping date
@receiver(pre_save, sender=Order)
def set_shipped_date(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now




# create Order Items Model
class OderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'



#automatically creating user shipping once they are register
def create_user_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_user_shipping, sender=User)

