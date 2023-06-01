from django.urls import path
from . import views

# app_name = 'app1'

urlpatterns = [
    path('', views.product_list, name="product-list"),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase-quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease-quantity'),

]
