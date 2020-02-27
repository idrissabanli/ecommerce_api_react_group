from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterAPIView

app_name = 'accounts'

urlpatterns = [
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
]