import pytest
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIRequestFactory

from backend.users.permissions import IsOwnerOrAdmin


@pytest.mark.django_db
class TestIsOwnerOrAdmin:
    """
    Test suite to verify the behavior of the `IsOwnerOrAdmin`
    permission class.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrAdmin()

    def test_admin_user_has_access(self, create_admin_user):
        """
        Admin (staff) users should ALWAYS have access.
        """
        admin_user = create_admin_user()
        request = self.factory.get('/')
        request.user = admin_user

        # pass the admin_user instance as the obj
        assert self.permission.has_object_permission(
            request, None, admin_user) is True

        # pass an AnonymousUser instance as the obj
        another_user = User.objects.create_user(
            username='another_user',
            password='testingPassword1234!',
        )

        assert self.permission.has_object_permission(
            request, None, another_user
        ) is True

    def test_owner_user_has_access(self, create_user):
        """
        A regular user should have access to ONLY their own
        object
        """
        user = create_user(username='john_doe')
        request = self.factory.get('/')
        request.user = user

        # permission is granted if obj == request.user
        assert self.permission.has_object_permission(
            request, None, user
        ) is True

    def test_non_owner_user_denied(self, create_user):
        """
        A regular user should NOT have access to another
        user's object.
        """
        user = create_user(username='user1')
        another_user = create_user(username='user2')
        request = self.factory.get('/')
        request.user = user

        assert self.permission.has_object_permission(
            request, None, another_user) is False

    def test_anonymous_user_denied(self, create_user):
        """
        An anonymous user should NOT have access to any object.
        """
        request = self.factory.get('/')
        request.user = AnonymousUser()

        # Passing any object (a dummy user) should result in False
        dummy_user = User(username='dummy')

        assert self.permission.has_object_permission(
            request, None, dummy_user) is False
