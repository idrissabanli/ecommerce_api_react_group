from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserProfileSerializer, ProfileUpdateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from accounts.utils import CustomSwaggerAutoSchema

User = get_user_model()


class LoginAPI(ObtainAuthToken):
    custom_serializer_class = UserProfileSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=AuthTokenSerializer,
                         responses={200: custom_serializer_class})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = self.custom_serializer_class(user, context={'request': request})
        # user_serializer.is_valid(raise_exception=True)
        return Response(user_serializer.data)


class ProfileAPIView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    update_serializer_class = ProfileUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response(data=self.serializer_class(request.user, context={'request': request}).data)

    @swagger_auto_schema(request_body=update_serializer_class, responses={200: UserProfileSerializer})
    def put(self, request):
        data = request.data
        serializer = self.update_serializer_class(request.user, data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return Response(data=self.serializer_class(updated_user, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=update_serializer_class, responses={200: UserProfileSerializer})
    def patch(self, request):
        data = request.data
        serializer = self.update_serializer_class(request.user, data=data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()
        return Response(data=self.serializer_class(updated_user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class RegisterAPIView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(auto_schema=CustomSwaggerAutoSchema, request_body=UserCreateSerializer,)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
