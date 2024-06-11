from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['client', 'announcement', 'question_client', 'reply', 'created', 'updated', 'active']
    search_fields = ['client__username', 'announcement__title', 'question_client', 'reply']
    list_filter = ['created', 'updated', 'active']
    ordering = ['created']
    readonly_fields = ['created', 'updated']