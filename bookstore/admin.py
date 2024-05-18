from django.contrib import admin
from .models import UserProfile, Address, UserAddress


# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'phone', 'photo', 'address']
    search_fields = ['user__username']  # Corrigido typo no search_fields


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
     list_display = ['cep', 'public_place', 'public_place_type', 'neighborhood', 'city', 'state']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'user', 'number', 'complement', 'nickname']
