import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to provide an instance of 
    Django Rest Framework's `APIClient`.

    This ensures all tests are isolated from each other.
    """
    return APIClient()


@pytest.fixture
def create_user(db) -> User:
    """
    Fixture to create a regular user
    """
    def make_user(**kwargs):
        username = kwargs.get('username', 'testuser')
        email = kwargs.get('email', 'testuser@example.com')
        password = kwargs.get('password', 'testpassword1234!')
        user = User.objects.create_user(
            username=username, email=email, password=password)
        return user
    return make_user


@pytest.fixture
def create_admin_user(db) -> User:
    """
    Fixture to create an admin user.
    """
    def make_admin_user(**kwargs):
        username = kwargs.get('username', 'admin')
        email = kwargs.get('email', 'admin@example.com')
        password = kwargs.get('password', 'adminpassword1234!')
        admin_user = User.objects.create_superuser(
            username=username, email=email, password=password)
        return admin_user
    return make_admin_user


@pytest.fixture
def authenticated_client(api_client, create_user) -> APIClient:
    """
    Fixture to provide an instance of `APIClient`
    authenticated as a regular user.
    """
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_authenticated_client(api_client, create_admin_user) -> APIClient:
    """
    Fixture to provide an instance of `APIClient`
    authenticated as an admin user.
    """
    admin_user = create_admin_user()
    api_client.force_authenticate(user=admin_user)
    return api_client
