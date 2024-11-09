from django.contrib import admin
from .models import Product, Announcement

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_area', 'published_at', 'author', 'seller']
    search_fields = ['name', 'author']  # Adicionado search_fields


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'condition', 'price', 'product', 'seller']
    search_fields = ['title', 'study_area']  # Adicionado search_fields
