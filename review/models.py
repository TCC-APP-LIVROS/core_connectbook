from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey('ads.Announcement', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    class Meta:
        unique_together = ('customer', 'announcement')  # Ensure only one review per user per announcement

    def __str__(self):
        return f"Review by {self.customer.username} for {self.announcement.title}"