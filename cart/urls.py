from django.urls import path
from .views import add_car

urlpatterns = [
    path('add/', add_car, name='add_car')
]
