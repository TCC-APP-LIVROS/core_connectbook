from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'announcement', 'rating', 'comment']
    search_fields = ['customer__username', 'announcement__title', 'comment']
    list_filter = ['rating']
    ordering = ['customer', 'announcement']
    readonly_fields = ['customer', 'announcement']