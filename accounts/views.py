from django.shortcuts import render,redirect
from .forms import RegistrationForm

from carts.models import Cart,CartItem

from carts.views import _cart_id

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Account,MyAccountManager
# Create your views here.

import requests

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user_name=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,email=email,password=password)
            user.phone_number=phone_number
            user.save()
            return redirect('login')



    else:
        form=RegistrationForm()
    context={
    'form': form
    }
    return render(request,'accounts/register.html',context)

def signin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
         
                cart_item_exists=CartItem.objects.filter(cart=cart).exists()

                
                if cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    product_variation=[] # existing cart
                    for item in cart_item:
                        variation=item.variation.all()
                        product_variation.append(list(variation))


                    cart_item=CartItem.objects.filter(user=user)

                    #Existing Variations -> Database
                    #Current Variation  -> GET Request (product_variation)
                    #Cart_id -> Database
                    exst_var=[]
                    id=[]
                    for item in cart_item:
                    
                        existing_variation=item.variation.all()
                        exst_var.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:    
                        if pr in exst_var:
                            #increase cart_item quantity
                            index=exst_var.index(pr)
                            id=id[index]
                            item=CartItem.objects.get(id=id )
                            item.user=user
                            item.quantity +=1 
                            item.save()


                        else:
                            cart_items=CartItem.objects.filter(cart=cart)

                            for cart_item in cart_items:
                                cart_item.user=user
                                cart_item.save()

            except Exception as e:
                print("Error in Exception" + str(e))
            auth.login(request,user)


            url=request.META.get('HTTP_REFERER')

            try:
                query=requests.utils.urlparse(url).query
                
                params=dict(x.split("=") for x in query.split("&"))
                
                return redirect(params['next'])
            except:
                return redirect('dashboard')

                
        else:
            return render(request,'accounts/login.html')

   
   
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard.html')