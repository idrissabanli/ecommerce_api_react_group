from django.urls import path
from .routers import router

app_name = 'blog'

urlpatterns = [
]

urlpatterns += router.urls