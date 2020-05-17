from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image', 'token']

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'image',]
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

