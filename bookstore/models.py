from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    cep = models.CharField(max_length=9, default='00000-000')
    public_place = models.CharField(max_length=255)
    public_place_type = models.CharField(max_length=100, default='default_type')
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, default='BA')

    def __str__(self):
        return f"{self.public_place}, {self.neighborhood}, {self.city}, {self.state} - CEP: {self.cep}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    email = models.EmailField(max_length=250, default="user@example.com")
    address = models.ForeignKey('UserAddress', on_delete=models.CASCADE, null=True, related_name='address_userprofile')

    def __str__(self):
        return self.user.username


class UserAddress(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, related_name='address_user')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_address')
    number = models.CharField(max_length=50)
    complement = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, Number: {self.number}, Complement: {self.complement}, Nickname: {self.nickname}"

