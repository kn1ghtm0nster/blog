import pytest
from django.urls import reverse, resolve
from users.views import UserListApi, UserDetailApi, UserUpdateApi, UserDeleteApi


@pytest.mark.django_db
class TestUserUrls:
    """
    Tests are to ensure that the URL patterns in `users/urls.py` 
    are correctly mapped to their corresponding view classes.
    """

    def test_user_list_url(self):
        """
        Confirm that `/users/` resolves to `UserListApi` and
        uses the name `user-list`.
        """
        path = reverse('user-list')
        resolver = resolve(path)
        assert resolver.view_name == 'user-list'
        assert resolver.func.view_class is UserListApi

    def test_user_detail_url(self):
        """
        Confirm  that `users/<int:pk>/` resolves to `UserDetailApi`
        and uses the `user-detail` name.
        """
        path = reverse('user-detail', kwargs={'pk': 1})
        resolver = resolve(path)
        assert resolver.view_name == 'user-detail'
        assert resolver.func.view_class is UserDetailApi

    def test_user_update_url(self):
        """
        Confirm that `users/<int:pk>/update/` resolves to `UserUpdateApi`
        and uses the `user-update` name.
        """
        path = reverse('user-update', kwargs={'pk': 2})
        resolver = resolve(path)
        assert resolver.view_name == 'user-update'
        assert resolver.func.view_class is UserUpdateApi

    def test_user_delete_url(self):
        """
        Confirm that `users/<int:pk>/delete/` resolves to `UserDeleteApi`
        and uses the `user-delete` name.
        """
        path = reverse('user-delete', kwargs={'pk': 3})
        resolver = resolve(path)
        assert resolver.view_name == 'user-delete'
        assert resolver.func.view_class is UserDeleteApi
