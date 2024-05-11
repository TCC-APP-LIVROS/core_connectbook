from django.urls import path
from .views import user_login, user_logout, profile_register, address_register, edit_profile, reset_password, user_address_register, create_product, create_announcement, edit_announcement

urlpatterns = [
    path('auth/login/', user_login, name='user-login'),
    path('auth/logout/', user_logout, name='user_logout'),
    path('auth/register/', profile_register, name='profile_register'),
    path('auth/register/address/', address_register, name='address_register'),
    path('auth/edit_profile/', edit_profile, name='edit_profile'),
    path('auth/reset_password/', reset_password, name='reset_password'),
    path('auth/user_address_register/', user_address_register, name='user_address_register'),
    path('ads/create_product/', create_product, name='create_product'),
    path('ads/create_announcement/', create_announcement, name='create_announcement'),
    path('ads/edit_announcement/', edit_announcement, name='edit_announcement')


]