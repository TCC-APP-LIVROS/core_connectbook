from django.urls import path
from .views import create_order, delete_order, order_detail

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('delete/', delete_order, name='delete_order'),
    path('list/<int:user_id>/<int:seller_id>/', order_detail, name='order_detail'),
]