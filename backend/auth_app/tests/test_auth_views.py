import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestRegisterUserApi:
    def test_register_user_successfully(self, client):
        url = reverse('register')
        data = {
            'username': 'user123',
            'email': 'user@example.com',
            'password': 'Password123!',
            'password2': 'Password123!'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        # Check the response data
        assert 'id' in response.json()
        assert response.json()['username'] == 'user123'
        assert response.json()['email'] == 'user@example.com'
        assert response.json()['admin'] is False
        assert 'token' in response.json()

    def test_register_duplicate_username(self, client, create_user):
        # Create initial user
        create_user(username='user123', email='user123@example.com',
                    password='Password@123')
        url = reverse('register')
        data = {
            'username': 'user123',
            'email': 'new_email@exampl.com',
            'password': 'NewPassword@123',
            'password2': 'NewPassword@123'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.json()

    def test_register_duplicate_email(self, client, create_user):
        create_user(username="user1",
                    email="uniqueemail@example.com", password="Pass123!")
        url = reverse('register')
        data = {
            "username": "user2",
            "email": "uniqueemail@example.com",
            "password": "Pass456!",
            "password2": "Pass456!"
        }
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.json()

    def test_register_password_mismatch(self, client):
        url = reverse('register')
        data = {
            'username': 'user123',
            'email': 'user3@example.com',
            'password': 'Pass123!',
            'password2': 'Pass1234!'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.json()

    def test_register_weak_password(self, client):
        url = reverse('register')
        data = {
            'username': 'user123',
            'email': 'weakpass@example.com',
            'password': 'short',
            'password2': 'short'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.json()


@pytest.mark.django_db
class TestObtainTokenApi:
    def test_obtain_token_successfully(self, client, create_user):
        create_user(username='tokenuser', email='token@example.com',
                    password='TokenPassword123!')
        url = reverse('token_obtain')
        data = {
            'username': 'tokenuser',
            'password': 'TokenPassword123!'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.json()

    def test_obtain_token_invalid_username(self, client, create_user):
        create_user(username='tokenuser', email='token@example.com',
                    password='TokenPassword123!')
        url = reverse('token_obtain')
        data = {
            'username': 'invaliduser',
            'password': 'TokenPassword123!'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.json()

    def test_obtain_token_invalid_password(self, client, create_user):
        create_user(username='tokenuser', email='token@example.com',
                    password='TokenPassword123!')
        url = reverse('token_obtain')
        data = {
            'username': 'tokenuser',
            'password': 'InvalidPassword123!'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.json()

    def test_obtain_token_missing_username(self, client):
        url = reverse('token_obtain')
        data = {
            'password': 'TokenPassword'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.json()

    def test_obtain_token_missing_password(self, client):
        url = reverse('token_obtain')
        data = {
            'username': 'tokenuser'
        }
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.json()
