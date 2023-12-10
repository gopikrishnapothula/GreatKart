from django.urls import path

from .views import register,signin,logout

urlpatterns=[
path('register/', register, name='register'),
path('login/', signin, name='login'),
path('logout/', logout, name='logout'),
]