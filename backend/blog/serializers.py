from rest_framework import serializers
from django.contrib.auth.models import User

from .models import BlogPost, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'parent',
                  'created_at', 'is_moderated']


class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model"""

    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author',
                  'allow_comments', 'created_at', 'updated_at', 'comments']
