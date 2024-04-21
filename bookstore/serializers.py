from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address, UserProfile, UserAddress


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    address = serializers.PrimaryKeyRelatedField(many=True, queryset=Address.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        address_data = validated_data.pop('address')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        for address in address_data:
            UserAddress.objects.create(user=user, address=address)
        return user