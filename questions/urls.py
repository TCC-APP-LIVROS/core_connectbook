from django.urls import path
from .views import list_questions, create_question, delete_question

urlpatterns = [
    path('list/', list_questions, name='list_questions'),
    path('create/', create_question, name='create_question'),
    path('delete/', delete_question, name='question_id'),
]