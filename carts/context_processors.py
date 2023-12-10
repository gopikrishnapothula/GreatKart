from .models import Cart,CartItem
from .views import _cart_id

def cart_count(request):
    count = 0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart)
        for item in cart_items:
            count += item.quantity
        

    except Cart.DoesNotExist:
        pass
    return dict(count=count)