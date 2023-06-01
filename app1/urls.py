from django.urls import path
from .views import *

urlpatterns = [
    path('',product_list,name="product-list"),
    path('product/<int:pk>/', product_detail, name='product-detail'),
]
