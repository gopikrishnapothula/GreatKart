from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':( 'product_name',)}
    list_display=('product_name','price','category','stock')


# Register your models here.
admin.site.register(Product,ProductAdmin)