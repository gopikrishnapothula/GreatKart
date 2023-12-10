from django.shortcuts import render,redirect,get_object_or_404

from .models import Cart,CartItem

from store.models import Product



# Create your views here.

def _cart_id(request):
    cart=request.session.session_key

    if not cart:
        cart=request.session.create()
    return cart




def add_cart(request,product_id):
    product=Product.objects.get(id=product_id) #get the product
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cartid created from session

    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()


    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,

        )
        cart_item.save()
    return redirect('cart')


def cart(request):
    try:
        prices={}
        total=0
        cart= Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
           
            total=total+ (cart_item.product.price * cart_item.quantity)
        
        tax=(5 * total)/100
        for cart_item in cart_items:    
            price=cart_item.product.price * cart_item.quantity 
            prices[cart_item]=price
        len= cart_items.count()

        context={
        'items':cart_items,
        'total': total,
        'tax': tax,
        'amount': total+ tax ,
        'price':prices,
        'len':len,
       
    }
    


    except Cart.DoesNotExist:
        return render(request, 'cart.html',{'len':0})
    
    return render(request, 'cart.html', context)



def decrease_cart(request,product_id):

    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    item=CartItem.objects.get(cart=cart,product=product)
    
    if item.quantity > 1:
        item.quantity=item.quantity-1
        item.save()
    else:
        item.delete()
    return redirect('cart')
 



def remove_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id=product_id)
    item=CartItem.objects.get(cart=cart,product=product)
    item.delete()
    return redirect('cart')


