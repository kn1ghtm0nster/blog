import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from backend.users.tests.conftest import admin_authenticated_client


@pytest.mark.django_db
class TestUserViews:
    """
    Tests for the user-related API views, leveraging
    fixtures from conftest.py to avoid repetitive setup.
    """

    def test_admin_can_list_users(self, admin_authenticated_client):
        """
        Admin users can list all existing users.
        """
        url = reverse('user-list')  # /api/users/
        response = admin_authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_non_admin_cannot_list_users(self, authenticated_client):
        """
        Non-admin users should not be able to list users.
        """
        url = reverse('user-list')  # /api/users/
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_can_view_own_details(self, authenticated_client, create_user):
        """
        A user can retrieve their own details via the API.
        """
        user = create_user(username='john_view', email='john_view@example.com')
        url = reverse('user-detail', kwargs={'pk': user.id})

        # Authenticate as the user
        authenticated_client.force_authenticate(user=user)
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('username') == 'john_view'

    def test_admin_can_view_any_user_details(self, admin_authenticated_client, create_user):
        """
        Admin users can view any existing user's details.
        """
        user = create_user(username='target_user', email='target@example.com')
        url = reverse('user-detail', kwargs={'pk': user.id})
        response = admin_authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('username') == 'target_user'

    def test_user_cannot_view_other_user_details(self, authenticated_client, create_user):
        """
        A user should NOT be able to view another user's details.
        """
        user1 = create_user(username='user1')
        user2 = create_user(username='user2')
        url = reverse('user-detail', kwargs={'pk': user2.id})

        authenticated_client.force_authenticate(user=user1)
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_can_update_own_profile(self, authenticated_client, create_user):
        """
        A user can update their own profile.
        """
        user = create_user(username='john_update')
        url = reverse('user-update', kwargs={'pk': user.id})

        authenticated_client.force_authenticate(user=user)
        response = authenticated_client.patch(
            url, data={'username': 'john_updated'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('username') == 'john_updated'

    def test_admin_can_update_any_profile(self, admin_authenticated_client, create_user):
        """
        Admin users can update any user's profile.
        """
        user = create_user(username='target_update')
        url = reverse('user-update', kwargs={'pk': user.id})

        response = admin_authenticated_client.patch(
            url, data={'username': 'target_updated_by_admin'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('username') == 'target_updated_by_admin'

    def test_user_cannot_delete_other_user(self, authenticated_client, create_user):
        """
        A regular user shuold NOT be able to delete another
        user's profile.
        """
        user1 = create_user(username='user1')
        user2 = create_user(username='user2')
        url = reverse('user-delete', kwargs={'pk': user2.id})

        authenticated_client.force_authenticate(user=user1)
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_any_user(self, admin_authenticated_client, create_user):
        """
        Admin users can delete any user's profile.
        """
        user = create_user(username='remove_me')
        url = reverse('user-delete', kwargs={'pk': user.id})

        response = admin_authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(username='remove_me').exists()
