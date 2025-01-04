from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BlogPost(models.Model):
    """Model for blog post"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model for a comment"""
    blog_post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    is_moderated = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog_post}'
