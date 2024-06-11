from django.contrib import admin
from .models import Itemcart


@admin.register(Itemcart)
class ItemcartAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product']
    search_fields = ['cart__id', 'product__title']
    list_filter = ['cart']
    ordering = ['cart']