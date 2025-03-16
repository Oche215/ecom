from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Shipping_full_name = models.CharField(max_length=200)
    Shipping_email = models.CharField(max_length=200)
    Shipping_address1 = models.CharField(max_length=200)
    Shipping_address2 = models.CharField(max_length=200)
    Shipping_city = models.CharField(max_length=200)
    Shipping_state = models.CharField(max_length=200, null=True, blank=True)
    Shipping_zipcode = models.CharField(max_length=200, null=True, blank=True)
    Shipping_country = models.CharField(max_length=200)

    #unpluralize Address
    class Meta:
        verbose_name_plural = "ShippingAddress"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'



