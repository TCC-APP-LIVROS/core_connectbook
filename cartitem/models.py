from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Itemcart(models.Model):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('ads.Product', on_delete=models.CASCADE, related_name='product_item')
    quantity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=None)

    class Meta:
        ordering = ('cart',)

    def __str__(self):
        return self.cart
