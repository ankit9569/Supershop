"""
URL configuration for supershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainapp.homePage,name="home"),
    path('about/',mainapp.aboutPage,name="about"),
    path('cart/',mainapp.cartPage,name="cart"),
    path('add-to-cart/',mainapp.addToCartPage,name="add-to-cart"),
    path('delete-cart/<str:id>/',mainapp.deleteCart,name="cart"),
    path('update-cart/<str:id>/<str:op>/',mainapp.updateCart,name="update-cart"),
    path('checkout/',mainapp.checkoutPage,name="checkout"),
    path('confirmation/',mainapp.confirmationPage,name="confirmation"),
    path('contact/',mainapp.contactPage,name="contact"),
    path('login/',mainapp.loginPage,name="login"),
    path('logout/',mainapp.logoutPage,name="logout"),
    path('signup/',mainapp.signupPage,name="signup"),
    path('shop/<str:mc>/<str:sc>/<str:br>/',mainapp.shopPage,name="shop"),
    path('singleproduct/<int:id>/',mainapp.singleproductPage,name="singleproduct"),
    path('profile/',mainapp.profilePage,name="profile"),
    path('update-profile/',mainapp.updateProfile,name="updateprofile"),
    path("add-to-wishlist/<int:id>/",mainapp.addToWishlistPage,name="add-to-wishlist"),
    path("deletewishlist/<int:id>/",mainapp.deleteWishlistPage,name="deletewishlist"),
    path("newsletter-subscribe/",mainapp.newsletterSubscribe,name="newsletter-subscribe"),
    path('reset-password-1/',mainapp.forgetPassword1Page,name="reset-password-1"),
    path('reset-password-2/',mainapp.forgetPassword2Page,name="reset-password-2"),
    path('reset-password-3/',mainapp.forgetPassword3Page,name="reset-password-3"),
    path('search/',mainapp.searchPage,name="search"),

    path('payment-success',mainapp.paymentSuccessPage,name="payment-success")

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
