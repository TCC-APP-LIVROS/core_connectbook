from django.db import models
from ads.models import Announcement
from django.contrib.auth.models import User

from auths.models import UserAddress 

class Order(models.Model):
    buyer = models.ForeignKey(User, related_name='user_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='user_seller', on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    quantity = models.IntegerField(default=1)

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