from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.template.context_processors import request

from django.views.generic import DetailView

from .models import Product, Category, UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress
from django.db.models import Count
from cart.cart import Cart
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserProfileForm
from django.db.models import Q
import json


# Create your views here.
def search(request):
    if request.method == 'POST':
        s = request.POST['searched']
        if s == '':
            messages.error(request, f'Your search entry cannot be empty {s}!')
            return render(request, 'search.html', {})
        else:
            searched = Product.objects.filter(Q(name__icontains=s) | Q(description__icontains=s) | Q(price__icontains=s) )
            if not searched:
                messages.success(request, f'Sorry, "{s}" did not return any result!')
                return render(request, 'search.html', {'s':s})
        return render(request, 'search.html', {'searched': searched, 's': s})

    else:

        products = Product.objects.all()
        return render(request, 'search.html', {'product': products})



def category_summary(request):
    categories = Category.objects.all()
    object_list = Product.objects.values('category').annotate(category_count=Count('category'))
    items = {'number_item': object_list.count()}
    return render(request, 'category/category_summary.html', {'categories': categories, 'items': items, 'object_list': object_list})

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        categories = Category.objects.get(name=foo)
        products = Product.objects.filter(category=categories)
        sales = Product.objects.filter(is_sale=True)
        return render(request, 'category/category.html', {'products': products, 'categories': categories, 'sales': sales})
    except:
        messages.success(request, "That category does not exist...")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = UserProfile.objects.get(user__id=request.user.id)
            carted = current_user.carted
            if carted:
                converted = json.loads(carted)
                cart = Cart(request)
                for key, value in converted.items():
                    cart.retrieve(product=key, quantity=value)

            messages.success(request, "Congratulations! You've successfully logged in.")
            return redirect('home')
        else:
            messages.success(request, "There's an error! Check your credentials and try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Congratulations! You have successfully signed up for a user account")
            return redirect('home')
        else:
            messages.success(request, "Congratulations! You have successfully signed up for a user account")
            return redirect('register/signup.html')
    else:
            return render(request, 'register/signup.html', {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'Your profile has been Updated!')
            return redirect('home')
        return render(request, 'register/update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'Your must be logged in to edit profile!')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            password_form = ChangePasswordForm(current_user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your password has been changed!')
                # login(request, current_user)
                return redirect('login')
            else:
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            password_form = ChangePasswordForm(current_user)
            return render(request, 'register/update_password.html', {'password_form': password_form})
    else:
        messages.success(request, 'Your must be logged in to edit password!')
        return redirect('home')


def update_profile(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        profile_form = UserProfileForm(request.POST or None, instance=current_user)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user )

        if profile_form.is_valid() or shipping_form.is_valid():
            profile_form.save()
            shipping_form.save()

            messages.success(request, 'Your profile information has been Updated!')
            return redirect('home')
        return render(request, 'register/update_profile.html', {'profile_form': profile_form, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'Your must be logged in to edit profile!')
        return redirect('home')

class UserDetail(DetailView):
    model = User
    template_name = 'register/profile.html'


def profile(request, pk):
    user = request.user
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=current_user.id)

        return render(request, 'register/profile.html', {'current_user': current_user, 'shipping_user': shipping_user, 'user':user })

    else:
        messages.success(request, 'You are not allowed to visit this page')
        return redirect('home')


def profile_info(request, pk):
    user = request.user
    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=user.id)
        shipping_user = ShippingAddress.objects.get(user__id=user.id)

        return render(request, 'register/profile_info.html', {'current_user': current_user, 'shipping_user': shipping_user, 'user':user })

    else:
        messages.success(request, 'You are not allowed to visit this page')
        return redirect('home')


def shipping_info(request, pk):
    user = request.user
    if request.user.is_authenticated:
        current_user = UserProfile.objects.filter(user__id=user.id)
        shipping_user = ShippingAddress.objects.get(user__id=user.id)

        return render(request, 'register/shipping_info.html', {'current_user': current_user, 'shipping_user': shipping_user, })

    else:
        messages.success(request, 'You are not allowed to visit this page')
        return redirect('home')


class UserDetail1(DetailView):
    model = UserProfile
    template_name = 'register/profile_info.html'


class UserDetail2(DetailView):

    model = ShippingAddress
    template_name = 'register/shipping_info.html'


def mikvah(request):
    return render(request, 'mikvah.html', {})