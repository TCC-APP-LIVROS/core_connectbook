from django.urls import path
from .views import add_car, edit_car, car_detail

urlpatterns = [
    path('add/', add_car, name='add_car'),
    path('edit/', edit_car, name='edit_car'),
    path('<int:id>/', car_detail, name='car_detail'),
]
