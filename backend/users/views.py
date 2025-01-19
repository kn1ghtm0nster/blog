from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User

from .serializers import UserSerializer


class UserPagination(PageNumberPagination):
    """
    Custom pagination class for user profiles
    """

    # number of user objects per page
    page_size = 10

    # query parameter for retrieving the next set of user objects
    page_size_query_param = 'page_size'

    # Maximum number of user objects that can be retrieved per page
    max_page_size = 100


class UserListApi(generics.ListAPIView):
    """
    API view to retrieve a paginated list of all
    users.
    Only accesible to `admin` users!
    """

    # order users by id and prefetch related blog posts and comments
    # to reduce the number of queries
    queryset = User.objects.all().order_by(
        'id').prefetch_related('blog_posts', 'comments')
    serializer_class = UserSerializer

    # restrict access to admin users
    permission_classes = [permissions.IsAdminUser]

    # apply custom pagination
    pagination_class = UserPagination
