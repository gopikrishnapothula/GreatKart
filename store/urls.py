
from django.urls import path
from .views import store,product_detail,search

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    
     path('', store,name='store'),
     path('category/<slug:category_slug>/', store, name='products_by_categories'),
     path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
     path('search/', search, name='search'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)