from django.urls import path
from .views import *

urlpatterns = [
    path('p',home),
    path('',product_list,name="product-list"),
]
