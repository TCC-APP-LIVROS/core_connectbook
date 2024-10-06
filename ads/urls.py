from django.urls import path
from .views import announcement_toggle_status, create_product, edit_product, delete_product, product_detail, list_product, create_announcement, edit_announcement, delete_announcement, announcement_detail, list_announcement, search_annoucement

urlpatterns = [
    path('product/create/', create_product, name='create_product'),
    path('product/edit/', edit_product, name='edit_product'),
    path('product/delete/', delete_product, name='delete_product'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/list/<int:page>/', list_product, name='list_product'),
    path('announcement/create/', create_announcement, name='create_announcement'),
    path('announcement/edit/', edit_announcement, name='edit_announcement'),
    path('announcement/delete/', delete_announcement, name='delete_announcement'),
    path('announcement/toggle/status/<int:announcement_id>', announcement_toggle_status, name='delete_announcement'),
    path('announcement/<int:announcement_id>/', announcement_detail, name='announcement_detail'),
    path('announcement/search/', search_annoucement, name='search_annoucement'),
    path('announcement/list/<int:page>/', list_announcement, name='list_announcement'),
]