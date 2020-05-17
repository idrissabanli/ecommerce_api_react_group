from blog.models import Blog, Blogger
from rest_framework import permissions
from blog.blog_api.serializers import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class BloggerViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Blogger.objects.all()
    serializer_class = BloggerSerializer


class BlogViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny,]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
