from rest_framework import serializers
from rest_framework import validators
from user_api.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('user_id', 'password', 'phone_number')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'password')


class LoginResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_id', )
