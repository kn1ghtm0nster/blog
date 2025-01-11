import pytest
from django.contrib.auth.models import User


@pytest.fixture
def create_user(db):
    def _create_user(username, email, password):
        user = User.objects.create_user(
            username=username, email=email, password=password)
        return user
    return _create_user
