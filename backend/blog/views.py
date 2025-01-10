# from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
# TODO remove and add real auth / permissions
from rest_framework.permissions import AllowAny

from .models import BlogPost
from .serializers import BlogPostSerializer


class BlogpostListApi(APIView):
    """
    View class to view all availble blog posts
    """

    permission_classes = [AllowAny]

    class OutputSerializer(serializers.ModelSerializer):
        """
        Serializer class for outgoing data to avoid data issues
        """

        class Meta:
            model = BlogPost
            fields = ['id', 'title', 'content', 'author',
                      'created_at', 'updated_at', 'allow_comments', 'comments']

    def get(self, request):
        posts = BlogPost.objects.all()
        serializer = self.OutputSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogpostCreateApi(APIView):
    """
    View class to create a new blog post
    """

    permission_classes = [AllowAny]

    class InputSerializer(serializers.ModelSerializer):
        """
        Serializer class for incoming data to avoid data issues
        """

        class Meta:
            model = BlogPost
            fields = ['title', 'content', 'author', 'allow_comments']

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
