from django.db import models


class Itemcart(models.Model):
    cart = models.ForeignKey('cart.Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('ads.Announcement', on_delete=models.CASCADE, related_name='product_item')

    class Meta:
        ordering = ('cart',)

    def __str__(self):
        return self.cart
