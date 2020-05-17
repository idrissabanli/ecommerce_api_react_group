from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserProfileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from accounts.utils import CustomSwaggerAutoSchema

class LoginAPI(ObtainAuthToken):
    custom_serializer_class = UserProfileSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=AuthTokenSerializer, responses={200: custom_serializer_class})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = self.custom_serializer_class(user, context={'request': request})
        # user_serializer.is_valid(raise_exception=True)
        return Response(user_serializer.data)

User = get_user_model()

class RegisterAPIView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=UserCreateSerializer,)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
