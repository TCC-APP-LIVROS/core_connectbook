from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, UserLogoutAPIView, UserPasswordResetAPIView

urlpatterns = [
    path('user/register/', UserCreateAPIView.as_view(), name='user-register'),
    path('user/login/', UserLoginAPIView.as_view(), name='user-login'),
    path('user/logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('user/password-reset/', UserPasswordResetAPIView.as_view(), name='user-password-reset'),
]