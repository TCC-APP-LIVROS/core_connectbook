from django.contrib import admin
from .models import UserProfile, Address


# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_diplay = ['user', 'email', 'phone', 'photo']
    search_fields = ['user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'number', 'complement', 'nickname']