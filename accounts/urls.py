from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterAPIView, LoginAPI, ProfileAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/user-profile/', ProfileAPIView.as_view(), name='api_user_profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]