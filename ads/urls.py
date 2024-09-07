from django.urls import path
from .views import create_product, create_announcement, edit_announcement

urlpatterns = [
    path('product/create/', create_product, name='create_product'),
    path('announcement/create/', create_announcement, name='create_announcement'),
    path('announcement/edit/', edit_announcement, name='edit_announcement')


]