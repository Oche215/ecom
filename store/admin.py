from django.contrib import admin
from django.contrib.auth.models import User
from django.template.defaultfilters import first

from store.models import Category, Customer, Product, Order, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(UserProfile)

#merge UserProfile and User info
class ProfileInLine(admin.StackedInline):
    model = UserProfile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email' ]
    inlines = [ProfileInLine]

#reregister User Model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


