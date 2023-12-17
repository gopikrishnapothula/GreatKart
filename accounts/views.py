from django.shortcuts import render,redirect
from .forms import RegistrationForm

from carts.models import Cart,CartItem

from carts.views import _cart_id

from django.contrib import auth

from .models import Account,MyAccountManager
# Create your views here.

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
         
                cart_items=CartItem.objects.filter(cart=cart, is_active=True)

                for cart_item in cart_items:
                    cart_item.user=user
                    cart_item.save()

            except:
                pass
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html')

   
   
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

