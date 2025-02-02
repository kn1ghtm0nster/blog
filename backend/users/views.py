from calendar import c
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.db import transaction
import logging

from .serializers import UserSerializer, UserUpdateSerializer
from .permissions import IsOwnerOrAdmin

# Initialize logger for this file
logger = logging.getLogger(__name__)


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


class UserDetailApi(generics.RetrieveAPIView):
    """
    API view to retrieve details of a single user.
    Accessible to the user themselves OR admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class UserUpdateApi(generics.UpdateAPIView):
    """
    API view to update a specific user's profile.
    Accessible to the user themselves OR admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_context(self):
        """
        Adds the request to the serializer context.
        This is needed for the serializer to access the requesting
        user.
        """

        # include ther request object (not done by default so override of this method is required)
        context = super(UserUpdateApi, self).get_serializer_context()
        context.update({'request': self.request})
        return context


class UserDeleteApi(generics.DestroyAPIView):
    """
    API view to delete a specific user's profile.
    Accessible by the user themselves or admin users.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    # Ensures the deletion is atomic (all or nothing)
    # If anything fails, the transaction is rolled back! :)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Handles the DELETE request to delete a user and all associated
        data.
        """
        try:
            user = self.get_object()  # retrieves the User object
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(user)
        response_data = {'message': 'deleted'}

        # Log deletion
        logger.info(f"User deleted: {user.username} deleted by {
                    request.user.username}.")

        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
