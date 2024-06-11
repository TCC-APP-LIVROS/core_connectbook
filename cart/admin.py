from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['client', 'product']
    search_fields = ['client__username', 'product__title']
    list_filter = ['client', 'product']
    ordering = ['product']