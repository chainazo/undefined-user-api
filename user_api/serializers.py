from rest_framework import serializers
from user_api.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password', 'phone_number')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
