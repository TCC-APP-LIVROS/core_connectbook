from django.urls import path
from .views import car_detail, delete_cart

urlpatterns = [
    path('add/', add_car, name='add_car'),
    path('edit/', edit_car, name='edit_car'),
    path('<int:cart_id>/', car_detail, name='car_detail'),
]
