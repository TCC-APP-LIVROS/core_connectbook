from django.urls import path
from .views import create_order, delete_order, order_detail

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('delete/', delete_order, name='delete_order'),
]