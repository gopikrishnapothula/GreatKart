from django.urls import path
from .views import cart,add_cart,decrease_cart,remove_item
urlpatterns=[
path('', cart, name='cart'),
path('add_cart/<int:product_id>/', add_cart, name='add_cart' ),
path('decrease_cart/<int:product_id>/<int:cart_id>/' , decrease_cart ,name='decrease_cart'),
path('remove_item/<int:product_id>/<int:cart_id>/' , remove_item ,name='remove_item'),
]