from re import M
import pytest
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

from auth_app.serializers import RegisterSerializer, TokenSerializer


@pytest.mark.django_db
class TestRegisterSerializer:
    def test_valid_registration_data(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'ValidPassword123!',
            'password2': 'ValidPassword123!'
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid() is True

        user = serializer.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.check_password('ValidPassword123!') is True

    def test_registration_password_mismatch(self):
        data = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'Pass123!',
            'password2': 'Pass124!'
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'password' in serializer.errors
        assert serializer.errors['password'] == ['Passwords did not match.']

    def test_registration_duplicate_username(self, create_user):
        create_user(username='existinguser',
                    email='existinguser@example.com', password='Pass123!')
        data = {
            'username': 'existinguser',
            'email': 'differentemail@example.com',
            'password': 'DifferentPass1!',
            'password2': 'DifferentPass1!'
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'username' in serializer.errors
        assert serializer.errors['username'][0] == 'A user with that username already exists.'

    def test_registration_duplicate_email(self, create_user):
        create_user(username='user1', email='unique@example.com',
                    password='Pass123!')
        data = {
            'username': 'user2',
            'email': 'unique@example.com',
            'password': 'Pass123!',
            'password2': 'Pass123!'
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'email' in serializer.errors
        assert serializer.errors['email'][0] == 'This field must be unique.'

    def test_registration_weak_password(self):
        data = {
            'username': 'weakpassuser',
            'email': 'weak@example.com',
            'password': 'short',
            'password2': 'short'
        }
        serializer = RegisterSerializer(data=data)

        assert serializer.is_valid() is False
        assert 'password' in serializer.errors
