from django.urls import path
from views import list_reviews, create_review, delete_review

urlpatterns = [
    path('list/', list_reviews, name='list_reviews'),
    path('create/', create_review, name='create_review'),
    path('delete/', delete_review, name='delete_review'),
]