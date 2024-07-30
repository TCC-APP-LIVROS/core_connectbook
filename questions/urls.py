from django.urls import path
from .views import list_questions, create_question

urlpatterns = [
    path('list/', list_questions, name='list_questions'),
    path('create/', create_question, name='create_question'),
]