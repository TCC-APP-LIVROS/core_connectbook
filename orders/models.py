from django.db import models
from cartitem.models import Itemcart
from ads.models import Announcement

class Order(models.Model):
    item_cart = models.ForeignKey(Itemcart, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=20, default='PENDING')

    def __str__(self):
        return f'Order #{self.id} - {self.status}'

    def finalize_order(self):
        # Reduz a quantidade do anúncia e desativa-o se chager a 0.

        announcement = self.announcement
        item_cart = self.item_cart

        if announcement.quantity >= item_cart.quantity:
            # Reduz a quantidade do anúncio pelo número de itens no carrinho
            announcement.quantity -= item_cart.quantity
            announcement.save()

            # Desativa o anúncio se a quantidade chegar a 0
            if announcement.quantity == 0:
                announcement.status = 'DISABLE'
                announcement.save()
            self.status = 'COMPLETED'
        else:
            # Lidar com a situação onde o estcoque não é suficiente
            self.status = 'FAILED'
        self.save()