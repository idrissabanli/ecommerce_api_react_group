from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image', 'token']

    def get_token(self, user):
        request = self.context.get('request')
        if request and hasattr(request, 'META') and request.META.get('HTTP_AUTHORIZATION'):
            header_token = request.META.get('HTTP_AUTHORIZATION')
            return header_token.split()[1]
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


class ProfileUpdateSerializer(serializers.ModelSerializer):

    def validate_email(self, value):
        request = self.context.get('request')
        user = request.user
        if value != user.email:
            raise serializers.ValidationError(_("You can not change your email"))
        return value

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image',]

