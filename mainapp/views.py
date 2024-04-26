from django.shortcuts import render,HttpResponseRedirect
from .models import *

from django.contrib.messages import success,error
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate 
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from random import randint

from razorpay import client

from django.conf import settings
from django.core.mail import send_mail


import razorpay

# Create your views here.

def homePage(Request):
    products=Product.objects.all().order_by("-id")[0:8]
    return render(Request,"index.html",{'products':products})


@login_required(login_url="/login/")
def aboutPage(Request):
    return render(Request,"about.html") 



def addToCartPage(Request):
    if(Request.method=="POST"):
        cart=Request.session.get("cart",None)
        qty=int(Request.POST.get("qty"))
        id=Request.POST.get("id")
        try:
            p=Product.objects.get(id=id)
            if(cart):
                if(str(id) in cart.keys()):
                    item=cart[str(id)]
                    item['qty']=item['qty']+int(qty)
                    item['total']=item['total']+int(qty)*item['price']
                    cart[str(id)]=item
                else:
                    cart.setdefault(str(id),{'productid':id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':int(qty)*p.finalprice,'pic':p.pic1.url})

            else:
                cart={str(id):{'productid':id,'name':p.name,'brand':p.brand.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':int(qty)*p.finalprice,'pic':p.pic1.url}}
            Request.session['cart']=cart
            Request.session.set_expiry(60*60*24*30)
        except:
            pass
    return HttpResponseRedirect("/cart/")


@login_required(login_url="/login/")
def cartPage(Request):
    cart=Request.session.get('cart',None)
    subtotal=0
    shipping=0
    total=0
    if(cart):
        for value in cart.values():
            subtotal=subtotal+value['total']
        if(subtotal>0 and subtotal<10000):
            shipping=150
        total=subtotal+shipping
    return render(Request,"cart.html",{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total})

def deleteCart(Request,id):
    cart=Request.session.get("cart",None)
    if(cart):
        del cart[id]
        Request.session['cart']=cart
    else:
        pass
    return HttpResponseRedirect("/cart/")

def updateCart(Request,id,op):
     cart=Request.session.get("cart",None)
     if(cart):
         item=cart[id]
         if(op=="dec" and item['qty']==1):
             return HttpResponseRedirect("/cart/")
         else:
             if(op=="dec"):
                 item['qty']=int(item['qty'])-1
                 item['total']=item['total']-item['price']
             else:
                 item['qty']=int(item['qty'])+1
                 item['total']=item['total']+item['price']
         cart[id]=item
         Request.session['cart']=cart
     else:
         pass
     return HttpResponseRedirect("/cart/")
         
    


@login_required(login_url="/login/")
def contactPage(Request):
    if(Request.method=="POST"):
        c=Contact()
        c.name=Request.POST.get("name")
        c.email=Request.POST.get("email")
        c.phone=Request.POST.get("phone")
        c.subject=Request.POST.get("subject")
        c.message=Request.POST.get
        ("message")
        c.save()
        success(Request,"Thanks to Share Your Query with Us And Our Team will contact you soon")
    return render(Request,"contact.html")

client=razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def checkoutPage(Request):
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        cart=Request.session.get('cart',None)
        subtotal=0
        shipping=0
        total=0
        if(cart):
            for value in cart.values():
                subtotal=subtotal+value['total']
            if(subtotal>0 and subtotal<1000):
                shipping=150
            total=subtotal+shipping
        if(Request.method=="POST"):
            mode=Request.POST.get("mode")
            checkout=Checkout()
            checkout.buyer=buyer
            checkout.subtotal=subtotal
            checkout.total=total
            checkout.shipping=shipping
            checkout.save()

            for key,value in cart.items():
                p=Product.objects.get(id=int(key))
                cp=CheckoutProduct()
                cp.checkout=checkout
                cp.product=p
                cp.qty=value['qty']
                cp.total=value['total']
                cp.save()
                Request.session['cart']={}
                if(mode=="COD"):
                    return HttpResponseRedirect("/confirmation/")
                else:
                    orderAmount=checkout.total*100
                    orderCurrency="INR"
                    paymentOrder=client.order.create(dict(amount=orderAmount,currency=orderCurrency))
                    paymentId=paymentOrder['id']
                    checkout.paymentmode=1
                    checkout.save()

                    return render(Request,"pay.html",{
                        'amount':orderAmount,
                        'api_key':settings.RAZORPAY_API_KEY,
                        'order_id':paymentId,
                        "User":buyer
                    })

        return render(Request,"checkout.html",{'buyer':buyer,'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total})
    except:
      pass



def paymentSuccessPage(Request,rppid):
    buyer=Buyer.objects.get(username=Request.user)
    check=Checkout.objects.filter(user=buyer)
    check=check[::-1]
    check=check[0]
    check.rppid=rppid
    check.paymentstatus=1
    check.save()
    return HttpResponseRedirect("/confirmation/")



def confirmationPage(Request):
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        cart=Request.session.get('cart',None)
        checkout=Checkout.objects.filter(buyer=buyer).order_by("-id").first()
        subtotal=0
        shipping=0
        total=0
        if(cart):
            for value in cart.values():
                subtotal=subtotal+value['total']
                if(subtotal>0 and subtotal<1000):
                    shipping=150
                total=subtotal +shipping
        Request.session['cart']={}
        return render(Request,"confirmation.html",{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total,'buyer':buyer,'checkout':checkout}) 
    
    except:
        return HttpResponseRedirect("/admin/")   

def loginPage(Request):
    if(Request.method=="POST"):
        username=Request.POST.get("username")
        password=Request.POST.get("password")
        user=authenticate(username=username,password=password)
        if(user is not None):
            login(Request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            error(Request,"Invalid username and password")
    return render(Request,"login.html")

def signupPage(Request):
    if(Request.method=="POST"):
        password=Request.POST.get("password")
        cpassword=Request.POST.get("cpassword")
        if(password==cpassword):
             username=Request.POST.get("username")
             email=Request.POST.get("email")
             name=Request.POST.get("name")
             try:
               User.objects.create_user(username=username,email=email,password=password,first_name=name)
               phone=Request.POST.get("phone")
               b=Buyer()
               b.name=name
               b.email=email
               b.username=username
               b.phone=phone
               b.save()
               return HttpResponseRedirect("/login/")
             except:
                 error(Request,"Username Already Taken")
    
        else:
            error(Request,"Password and Confirm Password doesnot matched")    
    return render(Request,"signup.html")

@login_required(login_url="/login/")
def shopPage(Request,mc,sc,br):
    if(mc=="All" and sc=="All" and br=="All"):
        products=Product.objects.all().order_by("-id")
    
    elif(mc!="All" and sc=="All" and br=="All"):
        products=Product.objects.filter(maincategory=MainCategory.objects.get(name=mc)).order_by("-id")

    elif(mc=="All" and sc!="All" and br=="All"):
        products=Product.objects.filter(subcategory=SubCategory.objects.get(name=sc)).order_by("-id")

    elif(mc=="All" and sc=="All" and br!="All"):
        products=Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("-id")

    elif(mc!="All" and sc!="All" and br=="All"):
        products=Product.objects.filter(maincategory=MainCategory.objects.get(name=mc),subcategory=SubCategory.objects.get(name=sc)).order_by("-id")

    elif(mc!="All" and sc=="All" and br!="All"):
        products=Product.objects.filter(maincategory=MainCategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("-id")

    elif(mc=="All" and sc!="All" and br!="All"):
        products=Product.objects.filter(subcategory=SubCategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by("-id")

    else:
        products=Product.objects.filter(maincategory=MainCategory.objects.get(name=mc),subcategory=SubCategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by("-id")



    maincategory=MainCategory.objects.all().order_by("-id")
    subcategory=SubCategory.objects.all().order_by("-id")
    brand=Brand.objects.all().order_by("-id")
    return render(Request,"shop.html",{'products':products,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':mc,'sc':sc,'br':br})


def searchPage(Request):
    search=Request.POST.get("search")
    try:
        maincategory=MainCategory.objects.get(name=search)
    except:
        maincategory=None

    try:
        subcategory=SubCategory.objects.get(name=search)
    except:
        subcategory=None

    try:
        brand=Brand.objects.get(name=search)
    except:
        brand=None

    products=Product.objects.filter(Q(name__icontains=search)|Q(maincategory=maincategory)|Q(subcategory=subcategory)|Q(brand=brand))
    if(Request.method=="POST"):
         maincategory=MainCategory.objects.all().order_by("-id")
         subcategory=SubCategory.objects.all().order_by("-id")
         brand=Brand.objects.all().order_by("-id")
         return render(Request,"shop.html",{'products':products,'maincategory':maincategory,'subcategory':subcategory,'brand':brand})
    else:
        return HttpResponseRedirect("/")





@login_required(login_url="/login/")
def singleproductPage(Request,id):
    product=Product.objects.get(id=id)
    return render(Request,"single-product.html",{'product':product})

@login_required(login_url="/login/")
def profilePage(Request):
       
       if(Request.user.is_superuser):
           return HttpResponseRedirect("/admin/") 
       username=Request.user.username
       try:
         buyer=Buyer.objects.get(username=username)
         wishlist=Wishlist.objects.filter(buyer=buyer)
         return render(Request,"profile.html",{'buyer':buyer,'wishlist':wishlist})
       except:
           return HttpResponseRedirect("/login/")
       


@login_required(login_url="/login/")
def updateProfile(Request):
       if(Request.user.is_superuser):
           return HttpResponseRedirect("/admin/")
       username=Request.user.username

       try:
         buyer=Buyer.objects.get(username=username)

         if(Request.method=="POST"):
             buyer.name=Request.POST.get("name")
             buyer.email=Request.POST.get("email")
             buyer.address=Request.POST.get("address")
             buyer.pin=Request.POST.get("pin")
             buyer.city=Request.POST.get("city")
             buyer.state=Request.POST.get("state")

             if(Request.FILES.get("pic")):
                 buyer.pic=Request.FILES.get("pic")
             buyer.save()
             return HttpResponseRedirect("/profile/")
         return render(Request,"updateProfile.html",{'buyer':buyer})
       except:
           return HttpResponseRedirect("/login/")

@login_required(login_url="/login/")
def logoutPage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")


@login_required(login_url="/login/")
def addToWishlistPage(Request,id):
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        product=Product.objects.get(id=id)
        try:
            w=Wishlist.objects.get(product=product,buyer=buyer)
        except:
            w=Wishlist()
            w.product=product
            w.buyer=buyer
            w.save()

    except:
        pass
    return HttpResponseRedirect("/profile")

@login_required(login_url="/login/")
def deleteWishlistPage(Request,id):
    try:
        w=Wishlist.objects.get(id=id)
        w.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")


def newsletterSubscribe(Request):
    if(Request.method=="POST"):
        email=Request.POST.get("email")
        n=Newsletter()
        n.email=email
        try:
            n.save()
            success(Request,"Thanks to Subscribe Our Newsletter Service!!!!")
        except:
            error(Request,"Your Email Id is Already taken")
        return HttpResponseRedirect("/")
    
    else:
       return  HttpResponseRedirect("/")



def forgetPassword1Page(Request):
    if(Request.method=="POST"):
        username=Request.POST.get("username")
        try:
            buyer=Buyer.objects.get(username=username)
            otp=randint(100000,9999999)
            buyer.otp=otp
            buyer.save()

            subject = 'Otp for Password Reset!!! Team-Supershop'
            message = """
                           Hello    """+buyer.name+"""
                          OTP for password reset is """+str(otp)+"""
                          Please never share to Anyone
                     """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [buyer.email, ]
            send_mail( subject, message, email_from, recipient_list)
            Request.session['reset-password-user']=buyer.username
            return HttpResponseRedirect("/reset-password-2/")
        except:
            error(Request,"User Name is not found in Our Data Record")
    return render(Request,"forget-password-1.html")


def forgetPassword2Page(Request):
    if(Request.method=="POST"):
        username=Request.session.get("reset-password-user")
        if(username):
            otp=int(Request.POST.get("otp"))
            buyer=Buyer.objects.get(username=username)
            if(otp==buyer.otp):
                return HttpResponseRedirect("/reset-password-3/")
            else:
                error(Request,"Invalid Otp")
        else:
            error(Request,"unauthorized Access")
    return render(Request,"forget-password-2.html")

def forgetPassword3Page(Request):
        username=Request.session.get("reset-password-user")
        if(username):
            password=Request.POST.get("password")
            cpassword=Request.POST.get("cpassword")
            if(password==cpassword):
                user=User.objects.get(username=username)
                user.set_password(password)
                user.save()
                # return HttpResponseRedirect("/login/")
            else:
                error(Request,"Password and confirm password does not matched")
        else:
            error(Request,"unauthorized Access")
        return render(Request,"forget-password-3.html")