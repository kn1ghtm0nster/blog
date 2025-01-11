import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_successfully(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='SecurePass123!'
        )

        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'testuser@example.com'
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password('SecurePass123!') is True

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='adminuser1',
            email='admin@example.com',
            password='AdminPass123!'
        )

        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_username_uniqueness(self):
        User.objects.create_user(
            username='uniqueuser',
            email='another@example.com',
            password='AnotherPass123!'
        )

        with pytest.raises(IntegrityError):
            # attempt to create another user with the same username
            User.objects.create_user(
                username='uniqueuser',
                email='another@example.com',
                password='AnotherPass123!'
            )

    def test_password_is_hashed(self):
        user = User.objects.create_user(
            username='secureuser',
            email='secure@example.com',
            password='SecurePass123!'
        )

        assert user.password != 'SecurePass123!'
        # Default hashing prefix in Django
        assert user.password.startswith('pbkdf2_')

    def test_string_representation(self):
        user = User.objects.create_user(
            username='stringuser',
            email='string@example.com',
            password='StringPass123!'
        )

        assert str(user) == 'stringuser'
