from django.urls import path
from .views import user_login, user_logout, profile_register, address_register, edit_profile, reset_password, user_address_register

urlpatterns = [
    path('login/', user_login, name='user-login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', profile_register, name='profile_register'),
    path('register/address/', address_register, name='address_register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('reset_password/', reset_password, name='reset_password'),
    path('user_address_register/', user_address_register, name='user_address_register')

]