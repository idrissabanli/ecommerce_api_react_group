from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterAPIView, LoginAPI, ProfileAPIView

app_name = 'accounts'

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/user-profile/', ProfileAPIView.as_view(), name='api_user_profile'),
]