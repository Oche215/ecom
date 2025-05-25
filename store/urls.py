from django.urls import path

from .views import (home, about, logout_user, login_user,
                    signup, product, category, category_summary, search,
                    update_user, update_password, update_profile, UserDetail, UserDetail1, UserDetail2, profile,
                    profile_info, shipping_info, mikvah)

urlpatterns = [
    path('mikvah/', mikvah, name="mikvah"),
    path('search/', search, name="search"),
    path('category_summary/', category_summary, name="category_summary"),
    path('category/<str:foo>', category, name="category"),
    path('product/<int:pk>', product, name="product"),
    path('update_user/', update_user, name="update_user"),
    path('profile/<int:pk>', profile, name="profile"),
    path('profile_info/<int:pk>', profile_info, name="profile_info"),
    path('shipping_info/<int:pk>', shipping_info, name="shipping_info"),
    path('update_profile/', update_profile, name="update_profile"),
    path('update_password/', update_password, name="update_password"),
    path('signup/', signup, name="signup"),
    path('logout/', logout_user, name="logout"),
    path('login/', login_user, name="login"),
    path('about/', about, name="about"),
    path('', home, name="home"),

]