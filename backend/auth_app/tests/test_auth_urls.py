import pytest
from django.urls import reverse, resolve
from rest_framework import status

from auth_app.views import RegisterUserApi, ObtainTokenApi


@pytest.mark.django_db
class TestAuthUrls:
    def test_register_url(self):
        url = reverse('register')
        assert resolve(url).func.view_class == RegisterUserApi

    def test_token_obtain_url(self):
        url = reverse('token_obtain')
        assert resolve(url).func.view_class == ObtainTokenApi

    def test_register_url_accepts_post(self, client):
        url = reverse('register')
        response = client.post(url)

        # ensure GET not allowed
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_token_obtain_url_accepts_post(self, client):
        url = reverse('token_obtain')
        response = client.post(url)

        # ensure GET not allowed
        assert response.status_code == status.HTTP_400_BAD_REQUEST
