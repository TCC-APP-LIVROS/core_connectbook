from django.contrib.auth.models import User
from django.db import models
import uuid


class Address(models.Model):
    cep = models.CharField(max_length=9, default='00000-000')
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default='BA')
    street = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.neighborhood}, {self.city}, {self.state} - CEP: {self.cep}"


class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    photo = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, default="user@example.com")
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, null=True, related_name='address_userprofile')

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, related_name='address_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
    number = models.CharField(max_length=50)
    complement = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, Number: {self.number}, Complement: {self.complement}, Nickname: {self.nickname}"