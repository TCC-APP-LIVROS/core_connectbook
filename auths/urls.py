from django.urls import path
from .views import user_address_update, user_login, profile_register, address_register, edit_profile, reset_password, user_address_register, user_address_list

urlpatterns = [
    path('login/', user_login, name='user-login'),
    path('register/', profile_register, name='profile_register'),
    path('register/address/', address_register, name='address_register'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('reset_password/', reset_password, name='reset_password'),
    path('user_address_register/', user_address_register, name='user_address_register'),
    path('user_address_update/<int:id>', user_address_update, name='user_address_update'),
    path('user_address/<int:user_id>/', user_address_list, name='user_address')
]