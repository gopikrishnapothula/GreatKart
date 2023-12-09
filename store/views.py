from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

from django.core.paginator import Paginator

# Create your views here.
def store(request,category_slug=None):

    if category_slug==None:

        products=Product.objects.filter(is_available=True)
        product_count=products.count()
    else:
        category_slug=get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=category_slug , is_available=True)
        product_count=products.count()


    paginator = Paginator(products,6)
    paginator_page=request.GET.get("page")
    paginator_products=paginator.get_page(paginator_page)

    context={
        'products':paginator_products,
        'product_count':product_count,
        
    }

    return render(request,'store\store.html',context=context)


def product_detail(request,category_slug,product_slug):
    
    products=Product.objects.get(category__slug=category_slug ,slug=product_slug)

    context={
        'products':products
    }

    return render(request,'store\product-detail.html',context)