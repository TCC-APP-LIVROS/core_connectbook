from django.contrib import admin
from .models import Product, Announcement

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'author', 'seller']
    search_fields = ['name', 'author']  # Adicionado search_fields


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'study_area', 'condition', 'price', 'product']
    search_fields = ['title', 'study_area']  # Adicionado search_fields
