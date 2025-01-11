import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_user_success(client):
    url = reverse('register')
    data = {
        'username': 'user123',
        'email': 'user@example.com',
        'password': 'Password123!',
        'password2': 'Password123!'
    }
    response = client.post(url, data, format='json')

    assert response.status_code == 201
    assert 'token' in response.json()


@pytest.mark.django_db
def test_register_duplicate_username(client, create_user):
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

    assert response.status_code == 400
    assert 'username' in response.json()
