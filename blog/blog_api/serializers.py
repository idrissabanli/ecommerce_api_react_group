from rest_framework import serializers
from blog.models import *

class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger
        fields = [
            'id',
            'full_name',
            'created_at',
            'updated_at',
        ]


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'short_description',
            'content',
            'blogger_full_name',
            'created_at',
            'updated_at',
        ]