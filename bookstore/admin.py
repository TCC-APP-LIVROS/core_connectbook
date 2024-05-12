from django.contrib import admin
from .models import UserProfile, Address, UserAddress, Product, Announcement, Question


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'author', 'seller']
    search_fields = ['name', 'author']  # Adicionado search_fields


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'study_area', 'condition', 'price', 'product']
    search_fields = ['title', 'study_area']  # Adicionado search_fields


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['client', 'announcement', 'question_client', 'reply', 'created', 'active']
    search_fields = ['client__username', 'announcement__title']  # Adicionado search_fields
