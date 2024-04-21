from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    complement = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='profile_addresses')
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s address"