from django.urls import path
from .views import create_product, create_announcement, edit_announcement, upload_image

urlpatterns = [
    path('create_product/', create_product, name='create_product'),
    path('create_announcement/', create_announcement, name='create_announcement'),
    path('edit_announcement/', edit_announcement, name='edit_announcement'),
    path('image/upload/', upload_image, name='upload')
]