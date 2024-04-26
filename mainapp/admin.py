from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(
#     (MainCategory,SubCategory,Brand,Product,Buyer,Wishlist,AddToCart,Checkout,CheckoutProduct,Newsletter,Contact)
#     )


## Model table ke form me aye


@admin.register(MainCategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display=("id","name")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display=("id","name")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=("id","name","pic")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("id","name","maincategory","subcategory","brand","color","size","baseprice","discount","finalprice","description","stock","pic1","pic2","pic3","pic4")


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display=("id","name","username","email","phone","address","pin","city","state","otp")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display=("id","buyer","product")



@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display=("id","buyer","orderstatus","paymentstatus","paymentmode","subtotal","shipping","total","date","rpid")


@admin.register(CheckoutProduct)
class CheckoutProductAdmin(admin.ModelAdmin):
    list_display=["id","checkout","product"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display=("id","email")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=("id","name","email","subject","message","status","date")