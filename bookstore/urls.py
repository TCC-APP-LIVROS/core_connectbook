from django.urls import path
from .views import user_login, user_logout, profile_register, address_register, edit_profile, reset_password

urlpatterns = [
    path('auth/login/', user_login, name='user-login'),
    path('auth/logout/', user_logout, name='user_logout'),
    path('auth/register/', profile_register, name='profile_register'),
    path('auth/register/address/', address_register, name='address_register'),
    path('auth/edit_profile/', edit_profile, name='edit_profile'),
    path('auth/reset_password/', reset_password, name='reset_password')

]