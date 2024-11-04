from django.urls import path
from .views import car_detail, delete_cart

urlpatterns = [
    path('<int:id>/', car_detail, name='car_detail'),
    path('delete', delete_cart, name='delete_cart')
]
