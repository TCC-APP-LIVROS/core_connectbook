from django.contrib import admin
from .models import Itemcart


@admin.register(Itemcart)
class ItemcartAdmin(admin.ModelAdmin):
    list_display = ['cart', 'announcement', 'quantity']
    search_fields = ['cart__id', 'announcement__title']
    list_filter = ['cart']
    ordering = ['cart']