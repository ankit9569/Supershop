from django import template

register=template.Library()

@register.filter(name="paymentMode")
def PaymentMode(Request,num):
    if(num==0):
        return "COD"
    else:
        return "NetBanking"