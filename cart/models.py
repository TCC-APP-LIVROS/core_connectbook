from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('client',)

    def __str__(self):
        return f"Carrinho de {self.client}"
