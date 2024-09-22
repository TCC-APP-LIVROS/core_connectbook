from django.urls import path
from .views import create_product, edit_product, delete_product, product_detail, list_product, create_announcement, edit_announcement, announcement_detail, list_announcement

urlpatterns = [
    path('product/create/', create_product, name='create_product'),
    path('product/edit/', edit_product, name='edit_product'),
    path('product/delete/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/list/<int:page>/', list_product, name='list_product'),
    path('announcement/create/', create_announcement, name='create_announcement'),
    path('announcement/edit/', edit_announcement, name='edit_announcement'),
    path('announcement/<int:id>/', announcement_detail, name='announcement_detail'),
    path('announcement/list/<int:page>/', list_announcement, name='list_announcement'),


]