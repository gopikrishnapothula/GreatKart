from django.shortcuts import render,redirect,get_object_or_404

from .models import Cart,CartItem

from store.models import Product,Variation

from django.http import HttpResponse


# Create your views here.

def _cart_id(request):
    cart=request.session.session_key

    if not cart:
        cart=request.session.create()
    return cart




def add_cart(request,product_id):
    
    product=Product.objects.get(id=product_id) #get the product
    product_variation=[]
    if request.method=='POST':

        for item in request.POST:
            key= item
            value=request.POST[key]

            try:

                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

       

    
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request)) # get the cart using cartid created from session

            

        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        
        
    
        cart.save()

        cart_item_exists=CartItem.objects.filter(cart=cart,product=product).exists()
        if cart_item_exists:
            if request.user.is_authenticated:
                cart_item=CartItem.objects.get(product=product,cart=cart)
                cart_item.quantity += 1
                cart_item.user=request.user
            
            else:
                cart_item=CartItem.objects.filter(product=product,cart=cart)

                #Existing Variations -> Database
                #Current Variation  -> GET Request (product_variation)
                #Cart_id -> Database

                for item in cart_item:
                    exst_var=[]
                    id=[]
                    existing_variation=item.variation.all()
                    exst_var.append(list(existing_variation))
                    id.append(item.id)
                
                if product_variation in exst_var:
                    #increase cart_item quantity
                    index=exst_var.index(product_variation)
                    id=id[index]
                    item=CartItem.objects.get(id=id ,product=product)
                    item.quantity +=1 
                    item.save()

                else:
                    #create new
        
                    item=CartItem.objects.create(product=product,quantity=1,cart=cart)

                    if len(product_variation)>0:
                        item.variation.clear()
                        item.variation.add(*product_variation)
                    item.save()


        else :
            cart_item=CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=1,

            )
            if len(product_variation)>0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)



            if request.user.is_authenticated:
                cart_item.user=request.user
            cart_item.save()
        return redirect('cart')


def cart(request):
    try:
        prices={}
        total=0

        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        else:
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



def decrease_cart(request,product_id,cart_id):

    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product, id=product_id)

    try:
        item=CartItem.objects.get(cart=cart,product=product,id=cart_id)
            
        if item.quantity > 1:
            item.quantity=item.quantity-1
            
            if request.user.is_authenticated:
                item.user=request.user
            
            item.save()
            
        else:
            item.delete()
    
    except:
        pass

    return redirect('cart')
 



def remove_item(request,product_id,cart_id):
    
    product=get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
            item=CartItem.objects.filter(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        item=CartItem.objects.get(cart=cart,product=product,id=cart_id)
    item.delete()
    return redirect('cart')


