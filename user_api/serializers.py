from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user_api.validators import *
from user_api.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('user_id', 'password', 'phone_number')


class UserCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=100, validators=[PasswordValidator()])
    phone_number = serializers.CharField(max_length=13, validators=[
                                         PhoneNumberValidator(), UniqueValidator(queryset=UserModel.objects.all())])
    age = serializers.IntegerField()
    gender = serializers.CharField(
        max_length=1, default='M', validators=[GenderValidator()])

    def create(self, validated_data):
        return UserModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raise AttributeError('Update not supported')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'password')


class LoginResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('user_id', )
