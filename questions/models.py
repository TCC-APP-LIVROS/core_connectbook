from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey('ads.Announcement', on_delete=models.CASCADE, related_name='questions')  # Alterado related_name
    question_client = models.TextField()
    reply = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.question_client