from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('ads.Announcement', on_delete=models.CASCADE)

    class Meta:
        ordering = ('product',)

    def __str__(self):
        return f"Product {self.product} added to cart"
