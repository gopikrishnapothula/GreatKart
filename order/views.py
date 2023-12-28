from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import datetime

import json

# Create your views here.
def place_order(request):
    current_user=request.user
    cart_item=CartItem.objects.filter(user=current_user)
    cart_count=cart_item.count()
    if cart_count<=0:
        return redirect('store')

    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()

            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.phone=form.cleaned_data['phone']
            data.address=form.cleaned_data['address']
            data.landmark=form.cleaned_data['landmark']
            data.pincode=form.cleaned_data['pincode']
            data.state=form.cleaned_data['state']
            data.user=current_user

            #to get the prices 
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
            total=0
            for cart_item in cart_items:
           
                total=total+ (cart_item.product.price * cart_item.quantity)
        
        
        
            tax=(5 * total)/100
            '''for cart_item in cart_items:    
                price=cart_item.product.price * cart_item.quantity 
                prices[cart_item]=price'''

            len= cart_items.count()


            data.order_total=total+tax
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            #Generate Order Number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+ str(data.id)
            data.order_number=order_number
            data.save()

            user_data=Order.objects.get(user=current_user,order_number=order_number,is_ordered=False)

            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
            total=0
            for cart_item in cart_items:
           
                total=total+ (cart_item.product.price * cart_item.quantity)
        
        
        
            tax=(5 * total)/100
            

            len= cart_items.count()


            context={

                'user_data': user_data,
                'items':cart_items,
                'total':total,
                'tax':tax,
                'amount':total+tax
            }
            return render(request,'orders\payments.html',context)
    else:
        return redirect('check_out')
    

def payments(request):
    body=json.loads(request.body)
    print(body)

    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        Payment_method=body['payment_method'],
        amount_paid=body['amount'],
        status=body['status'] ,
    )
    payment.save()
    order=Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    order.payment_id=payment
    order.is_ordered=True
    order.status="Completed"
    order.save()

    #move cart items to Order product table

    cart_items=CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product=OrderProduct()
        order_product.order=order
        order_product.payment=payment
        order_product.user=request.user
        order_product.product_id=item.product_id
        order_product.quantity=item.quantity
        order_product.product_price=item.product.price
        order_product.ordered=True

        order_product.save()

        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variation.all()
        product_item=OrderProduct.objects.get(id=order_product.id)
        product_item.variation.set(product_variation)
        product_item.save()

        # reduce quantity of sold product.

    
        item=Product.objects.get(id=product_item.product_id)
        item.stock -= product_item.quantity
        print(item.stock)
        item.save()


    CartItem.objects.filter(user=request.user).delete()

    data={
        "order_number" : order.order_number,
        'transId': payment.payment_id
    }


    return JsonResponse(data)


def order_complete(request):
    order_number=request.GET.get('order_number')
    payment_id=request.GET.get('payment_id')
    order=Order.objects.get(order_number=order_number)
    payment=Payment.objects.get(payment_id=payment_id)
    order_product=OrderProduct.objects.filter(order__order_number=order_number)
    subtotal=order.order_total - order.tax
    context={
        'order' : order,
        'payment':payment,
        'order_product':order_product,
        'subtotal':subtotal,

    }
    return render(request,'orders/order_complete.html',context)