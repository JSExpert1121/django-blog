from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings

from .models import User
import jwt


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'password', 'username',)
        read_only_fields = ('id', 'username',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=512, read_only=True)
    refresh_token = serializers.CharField(max_length=512, read_only=True)

    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError(
                'Email address is requied to login')

        if not password:
            raise serializers.ValidationError('Password is required to login')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError(
                'Username and password was not found')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')

        return {
            "username": user.username,
            "access_token": user.access_token,
            "refresh_token": user.refresh_token
        }


class LogoutSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=512, required=True)


class RefreshSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=512, read_only=True)
    refresh_token = serializers.CharField(max_length=512, write_only=True)

    def validate(self, data):
        refresh = data.get('refresh_token', None)

        if not refresh:
            raise serializers.ValidationError(
                'Refresh token is requied')

        try:
            payload = jwt.decode(refresh, settings.JWT_SECRETE_KEY)
            user_id = payload.get('id', None)
        except:
            raise serializers.ValidationError('Invalid refresh token')

        try:
            user = User.objects.get(pk=user_id)
        except:
            raise serializers.ValidationError('Invalid user id')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')

        return {
            "access_token": user.access_token,
        }


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
