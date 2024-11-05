from django.urls import path
from .views import create_order, delete_order, order_cancel, order_details, order_list

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('delete/', delete_order, name='delete_order'),
    path('list/<int:user_id>/<str:mode>/', order_list, name='order_list'),
    path('detail/<int:order_id>/<str:mode>/', order_details, name='order_details'),
    path('cancel/<int:order_id>/<str:mode>/', order_cancel, name='order_details'),
]