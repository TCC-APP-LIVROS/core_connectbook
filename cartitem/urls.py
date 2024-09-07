from django.urls import path
from .views import add_item_cart

urlpatterns = [
    path('add/', add_item_cart, name='add_item_cart')
]
