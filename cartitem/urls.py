from django.urls import path
from .views import add_item_cart, edit_item_cart, delete_item_cart, item_cart_detail

urlpatterns = [
    path('add/', add_item_cart, name='add_item_cart'),
    path('edit/', edit_item_cart, name='edit_item_cart'),
    path('delete/', delete_item_cart, name='delete_item_cart'),
    path('<int:id>/', item_cart_detail, name='item_cart_detail')

]
